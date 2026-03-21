from . import db

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), unique=True)
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    year = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    skills = db.Column(db.String(300))
    bio = db.Column(db.Text)
    resume_path = db.Column(db.String(200))
    profile_pic = db.Column(db.String(200))
    is_placed = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='student')
    applications = db.relationship('Application', backref='student')