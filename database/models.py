# database/models.py
from database.db import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_owner = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    revised_end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False)
