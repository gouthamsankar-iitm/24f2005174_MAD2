from . import db
from datetime import datetime

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    job_type = db.Column(db.String(50))        # Full-time / Internship
    location = db.Column(db.String(100))
    package = db.Column(db.Float)              # CTC
    eligible_branch = db.Column(db.String(100))
    eligible_cgpa = db.Column(db.Float)
    eligible_year = db.Column(db.Integer)
    vacancy = db.Column(db.Integer)
    rounds = db.Column(db.String(200))         # "Aptitude, Technical, HR"
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending/Approved/Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='drive')