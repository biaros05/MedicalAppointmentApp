import datetime
from .user import MedicalPatient, User


class Note:
    def __init__(self, patient, note_taker, note_date, note, attachement_path=[], id=None):
        if id != None and not isinstance(id, int):
            raise TypeError("Illegal type for id")
        if not isinstance(patient, MedicalPatient):
            raise TypeError("Illegal type for patient")
        if not isinstance(note_taker, User):
            raise TypeError("Illegal type for note taker")
        if note_taker.access_level != 'STAFF':
            raise TypeError("Notes can only be taken by doctors")
        if not isinstance(note_date, datetime.date):
            raise TypeError("Illegal type for note date")
        if not isinstance(note, str):
            raise TypeError("Illegal type for note")
        if attachement_path != None and not isinstance(attachement_path, list):
            raise TypeError("Illegal type for attachement_path")

        self.id = id
        self.patient = patient
        self.note_taker = note_taker
        self.note_date = note_date
        self.note = note
        self.attachement_path = attachement_path

    def to_json(self, prepended_url=None):
        data = {
            'patient': self.patient.to_json(prepended_url),
            'note_taker': self.note_taker.to_json(prepended_url),
            'note_date': self.note_date.isoformat(),
            'note': self.note,
            'attachment_path': self.attachement_path
        }
        if self.id is not None:
            data['id'] = self.id
        return data
  

    
