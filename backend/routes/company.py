from flask import Blueprint, request, jsonify, session
from models import db, Company, PlacementDrive, Application
from datetime import datetime

company_bp = Blueprint('company', __name__)

@company_bp.route('/company/drive/create', methods=['POST'])
def create_drive():

    if 'user_id' not in session or session.get('role') != 'company':
        return jsonify({"error": "Unauthorized"}), 401

    company = Company.query.filter_by(user_id=session['user_id']).first()
    data = request.json

    try:
        drive = PlacementDrive(
            company_id=company.id,
            job_title=data['job_title'],
            job_description=data.get('job_description'),
            job_type=data.get('job_type'),
            location=data.get('location'),
            package=data.get('package'),
            eligible_branch=data.get('eligible_branch'),
            eligible_cgpa=data.get('eligible_cgpa'),
            eligible_year=data.get('eligible_year'),
            vacancy=data.get('vacancy'),
            rounds=data.get('rounds'),
            deadline=datetime.strptime(data['deadline'], "%d-%m-%Y"),
            status="Pending"
        )
        db.session.add(drive)
        db.session.commit()

        return jsonify({"message": "Drive created, waiting for admin approval"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@company_bp.route('/company/drives', methods = ['GET'])
def company_drives():
    company = Company.query.filter_by(user_id  = session[user_id]).first()
    drives = PlacementDrive.query.filter_by(company_id = company.id).all()
    result = []

    for drive in drives:
        result.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "location": drive.location,
            "package": drive.package,
            "status": drive.status,
            "deadline": drive.deadline.strftime("%d-%m-%Y"),
            "applicant_count": Application.query.filter_by(drive_id=drive.id).count()
        })

@company_bp.route('/company/drive/<int:drive_id>/applications', methods=['GET'])
def get_applications(drive_id):

    if 'user_id' not in session or session.get('role') != 'company':
        return jsonify({"error": "Unauthorized"}), 401

    drive = PlacementDrive.query.get(drive_id)
    applications = drive.applications

    result = []
    #base_url = request.host_url

    for app in applications:
        student = app.student #??

        result.append({
            "application_id": app.id,
            "student_id": student.id,
            "name": student.name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "skills": student.skills,
            "status": app.status,
            #"resume": f"{base_url}uploads/{student.resume_path}" if student.resume_path else None,
            #"profile_pic": f"{base_url}uploads/{student.profile_pic}" if student.profile_pic else None,
            "phone": student.phone
        })

    return jsonify(result)