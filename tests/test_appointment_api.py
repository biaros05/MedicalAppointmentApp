from datetime import datetime
import json
import unittest
from flask import jsonify
from flask_login import current_user, login_user
from oracledb import DatabaseError
from MedicalApp import create_app
from MedicalApp.appointments import Appointments
from unittest.mock import patch


class AppointmentAPITestCases(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_get_appointments_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/appointments', headers=headers, follow_redirects=True)
        self.assertEqual(200, result.status_code) 


    def test_get_appointments_by_page_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/appointments', headers=headers, follow_redirects=True)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertTrue(len(results) > 0)

    def test_create_appointment_success_patient(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 9,
            "appointment_time": "2024-05-16",
            "description": "Routine check-up"
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(201, result.status_code)
        appointment = result.json
        self.assertEqual(data['description'], appointment['description'])

    def test_create_appointment_success_staff(self):
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 9,
            "appointment_time": "2024-05-16",
            "description": "Follow-up visit",
            "patient_id": 6,
            "location": "101"
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(201, result.status_code)
        appointment = result.json
        self.assertEqual(data['description'], appointment['description'])
        print(appointment['location'])
        self.assertEqual(data['location'], appointment['location'].split("/")[-1])

    def test_create_appointment_missing_fields(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {}
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)

    def test_create_appointment_invalid_patient_id(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE" 
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 1,
            "appointment_time": "2024-05-16T10:00:00",
            "description": "Routine check-up",
            "patient_id": "invalid"  
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)

    def test_create_appointment_invalid_doctor_id(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": "invalid",
            "appointment_time": "2024-05-16",
            "description": "Routine check-up"
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)

    def test_create_appointment_nonexistent_patient(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE" 
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 1,
            "appointment_time": "2024-05-16T10:00:00",
            "description": "Routine check-up",
            "patient_id": 999  
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)

    def test_create_appointment_nonexistent_doctor(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 999,
            "appointment_time": "2024-05-16",
            "description": "Routine check-up"
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)

    def test_create_appointment_invalid_description(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"  
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 1,
            "appointment_time": "2024-05-16T10:00:00",
            "description": "", 
            "patient_id": 2
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)


    def test_create_appointment_invalid_date_format(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 1,
            "appointment_time": "16-05-2024",
            "description": "Routine check-up"
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)

    def test_get_appointments_no_results(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/appointments?page=999', headers=headers, follow_redirects=True)
        self.assertEqual(404, result.status_code)

    def test_invalid_token(self):
        headers = {'Authorization': 'Bearer invalid_token', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 1,
            "appointment_time": "2024-05-16",
            "description": "Routine check-up"
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(401, result.status_code)

    def test_invalid_json_data(self):
        token = "valid_token"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {}
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(401, result.status_code)

    def test_unauthorized_patient_access(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 1,
            "appointment_time": "2024-05-16",
            "description": "Routine check-up"
        }
        result = self.client.post('/api/appointments', headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(400, result.status_code)

    def test_unauthorized_staff_access(self):
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1gn"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {
            "doctor_id": 1,
            "appointment_time": "2024-05-16",
            "description": "Follow-up visit"
        }

if __name__ == '__main__':
    unittest.main()
