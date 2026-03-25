from flask import Blueprint, request, jsonify, session
from models import db, User, Company, Student, PlacementDrive

student_bp = Blueprint('student', __name__)

@student_bp.route('/student/drives', methods=['GET'])
def view_drives():

    student = Student.query.filter_by(user_id=session['user_id']).first()

    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.eligible_year == student.year,
        PlacementDrive.eligible_branch == student.branch,
    ).all()
    result = []

    for drive in drives:
        result.append({
            "id": drive.id,
            "company": drive.company.name,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "job_type": drive.job_type,
            "package": drive.package,
            "location": drive.location,
            "eligible_branch": drive.eligible_branch,
            "eligible_cgpa": drive.eligible_cgpa,
            "eligible_year": drive.eligible_year,
            "vacancy": drive.vacancy,
            "rounds": drive.rounds,
            "deadline": drive.deadline.strftime("%d-%m-%Y"),
            "isEligible": (student.cgpa >= drive.eligible_cgpa) 
        })

    return jsonify(result)