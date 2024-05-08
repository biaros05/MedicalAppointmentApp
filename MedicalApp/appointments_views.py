from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.appointments import Appointments
from .forms import AppointmentForm, AppointmentResponseForm
from .db.dbmanager import get_db

bp = Blueprint('appointments', __name__, url_prefix='/appointments/')

def patient_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'PATIENT' and current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def doctor_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('/')
@login_required
@patient_access
def view_appointments():
    appointments = get_db().get_patient_appointments(current_user.id)
    return render_template('patient_appointments.html', appointments=appointments)

@bp.route('/book/', methods=['GET', 'POST'])
@login_required
@patient_access
def book_appointment():
    try:
        db = get_db()
        appointments = db.get_appointments()
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect('home.index')
    if appointments is None or len(appointments) == 0:
        abort(404)
    hide_patient = False
    form = AppointmentForm()
    form.set_patients()
    form.set_doctors()
    if current_user.access_level != 'STAFF':
        hide_patient = True
        form.patient.data = str(current_user.id)
        form.patient.render_kw = {'disabled' : ''} 
        form.set_doctors()
    form.set_rooms()
    if request.method == "POST" and form.validate_on_submit():
        try:
            patient = get_db().get_patients_by_id(form.patient.data)
            doctor = get_db().get_user_by_id(form.doctor.data)
        except DatabaseError as e:
            flash("something went wrong with the database")
            return redirect('home.index')
        status = 0
        time = form.appointment_time.data
        if doctor.id == current_user.id:
            status = 1
        location = form.location.data
        description = form.description.data
        
        new_appointment = Appointments(
            patient, doctor, time, status, location, description)

        new_id = db.add_appointment(new_appointment)
        flash("Appointement added to the List of Appointments")

        return redirect(
            url_for('appointments.get_appointment', id=new_id))

    return render_template('appointments.html', form=form, hide_patient=hide_patient)

@bp.route('/<int:id>/')
@login_required
@patient_access
def get_appointment(id):
    try:
        db = get_db()
        appointment = db.get_appointment_by_id(id)
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect('home.index')
    if appointment is None:
        flash("Appointment cannot be found", 'error')
        return redirect(url_for('appointments.book_appointment'))
    return render_template('specific_appointment.html', appointment=appointment)


@bp.route('/confirmed/<string:user_type>/')
@login_required
@patient_access
def confirmed_appointments(user_type):
    if user_type not in ('doctor', 'patient'):
        flash("Incorrect user type")
        return redirect(url_for('home.index'))
    try:
        appointments = None
        try:
            if user_type == 'doctor':
                appointments = get_db().get_appointments_by_status_doctor(1, current_user.id)
            if user_type == 'patient':
                appointments = get_db().get_appointments_by_status_patient(1, current_user.id)
        except DatabaseError as e:
            flash("something went wrong with the database")
            return redirect('home.index')
        if appointments is None or len(appointments) == 0:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('confirmed_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/<string:user_type>/')
@login_required
@patient_access
def requested_appointments(user_type):
    if user_type not in ('doctor', 'patient'):
        flash("Incorrect user type")
        return redirect(url_for('home.index'))
    try:
        appointments = None
        try:
            if user_type == 'doctor':
                appointments = get_db().get_appointments_by_status_doctor(0, current_user.id)
            if user_type == 'patient':
                appointments = get_db().get_appointments_by_status_patient(0, current_user.id)
        except DatabaseError as e:
            flash("something went wrong with the database")
            return redirect('home.index')
        if appointments is None or len(appointments) == 0:
            flash("No requested appointments")
            return redirect(url_for(f'{user_type}.dashboard'))
        return render_template('requested_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for(f'{user_type}.dashboard'))

# CHANGE!!!
@bp.route('/requests/<int:id>/', methods=['GET', 'POST'])
@login_required
@patient_access
def update_appointment(id):
    form = AppointmentResponseForm()
    form.set_choices()
    try:
        appointment = get_db().get_appointment_by_id(id)
        if request.method == 'POST' and form.validate_on_submit():
            status = form.select_confirmation.data
            room = form.room.data
            try:
                get_db().update_appointment_status(id, status, room=room)
                flash("Appointment has been successfully updated")
                return redirect(url_for('doctor.requested_appointments'))
            except DatabaseError:
                flash("Something went wrong with the database")
                return redirect(url_for('doctor.requested_appointments'))
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect('doctor.requested_appointments')
    except TypeError as e:
        flash("incorrect types")
        return redirect('doctor.requested_appointments')
    except ValueError as e: 
        flash("Incorrect values were passed")
        return redirect('doctor.requested_appointments')

    if appointment is None:
        abort(404, "This address does not exist")
    return render_template('specific_appointment.html', appointment=appointment, form=form)
