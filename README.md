
# Medical Appointment App

## Web URL to website:
http://10.172.19.22:5050/
will work by using Dawson College Wi-Fi or connecting through Forti VPN

## Gitlab repo
https://gitlab.com/csy2dawson23-24/420/section-3/1936038/medicalappointmentgroup02

## Project Name:
Medical App

## Project members
Tan-Jackson Tran, Student ID: 1936038
Haris Hussain, Student ID: 2234354
Sriraam Nadarajah, Student ID: 2245165
Bianca Rossetti, Student ID: 2233420

## Group Number 
Group 02


### developpers step :
1. Create virtual environment

```
python -m venv .venv
```

2. Activate virtual environment
```
2.1 Windows: .venv\Scripts\activate
2.2 Linux: source .venv/Scripts/activate
```

3. Install requirements:
```
pip install -r requirements.txt
```
4. Set up environment variables:
FLASK_SECRET, DBUSER, DBPWD

5. Install the Database:

flask --app MedicalApp init-Debug

You are ready to develop!

## Run and Debug (for devs)
```
flask --app MedicalApp run
```


## Deployment Steps:


# API Route:

You have to be logged in as any type of user beside a user thats 'BLOCKED' to be able to see the api


#### Get List of Doctors
- **Endpoint:** `/api/doctors/`
- **Method:** GET
- **Description:** Retrieves a paginated list of doctors, optionally filtered by first or last name.
- **Parameters:**
  - `page` (optional): The page number for pagination.
  - `first` (optional): Filter by the doctor's first name.
  - `last` (optional): Filter by the doctor's last name.

### Patient API Documentation

#### Get List of Patients
- **Endpoint:** `/api/patients`
- **Method:** GET
- **Description:** Retrieves a paginated list of patients, optionally filtered by first or last name.
- **Parameters:**
  - `page` (optional): The page number for pagination.
  - `first` (optional): Filter by the patient's first name.
  - `last` (optional): Filter by the patient's last name.
- **Authentication Required:** Yes
- **Access Required:** PATIENT, STAFF, or ADMIN

## Allergy API Documentation

### Get List of Allergies
- **Endpoint:** `/api/allergies`
- **Method:** GET
- **Description:** Retrieves a paginated list of allergies, optionally filtered by allergy name.
- **Parameters:**
  - `page` (optional): The page number for pagination.
  - `name` (optional): Filter by the allergy's name.
- **Authentication Required:** Yes
- **Access Required:** PATIENT, STAFF, or ADMIN

### Get Allergy Details
- **Endpoint:** `/api/allergies/<int:allergy_id>`
- **Method:** GET
- **Description:** Retrieves detailed information about a specific allergy by its ID.
- **Parameters:**
  - `allergy_id` (int): The ID of the allergy.
- **Authentication Required:** Yes
- **Access Required:** PATIENT, STAFF, or ADMIN

## Appointments API Documentation

### Endpoints Overview
This API allows for managing appointments, including creating, retrieving, updating, and deleting appointment records.

### General Information
- **Authentication Required:** Yes
- **Access Levels Required:** Depending on the action, access is required at different levels (PATIENT, STAFF, ADMIN).

### API Endpoints

#### Get or Create Appointments
- **Endpoint:** `/api/appointments/`
- **Methods:** GET, POST
- **Description:** 
  - **GET:** Retrieves a list of appointments with optional filtering and pagination.
  - **POST:** Creates a new appointment based on provided JSON payload.
- **Parameters for GET:**
  - `page` (optional): Specifies the page number in paginated results.
  - Additional query parameters can filter results based on doctor's or patient's first and last name.
- **Data Fields for POST:**
  - `doctor_id`: ID of the doctor involved in the appointment.
  - `appointment_time`: Scheduled time of the appointment.
  - `description`: Description or notes about the appointment.

#### Get, Update, or Delete Specific Appointment
- **Endpoint:** `/api/appointments/<int:id>`
- **Methods:** GET, PUT, DELETE
- **Description:** 
  - **GET:** Retrieves detailed information about a specific appointment.
  - **PUT:** Updates an existing appointment; fields that can be updated depend on the user's role.
  - **DELETE:** Deletes an appointment; typically requires ADMIN or STAFF level access.
- **Parameters:**
  - `id` (int): The ID of the appointment to retrieve, update, or delete.

### Error Codes and Messages
- **400 Bad Request:** Often returned when there are issues with the input data format or missing required fields.
- **401 Unauthorized:** Returned when a user is not authenticated.
- **403 Forbidden:** Returned when a user does not have permission to perform the requested action.
- **404 Not Found:** Returned when a requested entity (e.g., appointment, doctor, patient) is not found.
- **409 Conflict:** General database error, e.g., when there is an error during a database operation.

### Data Handling Practices
- All inputs are validated for type and format.
- Access controls are enforced based on user roles.

### Updates and Modifications
- Appointments can be modified only by users with appropriate permissions, and certain fields may be locked based on the user's role.
- Deleting an appointment requires specific roles and is permanently removed from the database upon action.
