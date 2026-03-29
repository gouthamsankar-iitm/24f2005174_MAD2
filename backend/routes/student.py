from flask import Blueprint, request, jsonify, session
from models import db, User, Company, Student, PlacementDrive, Application
import os
from flask import current_app 
from flask import send_from_directory

student_bp = Blueprint('student', __name__)

@student_bp.route('/student/drives', methods=['GET'])
def view_drives():

    if 'user_id' not in session or session.get('role') != 'student':
        return jsonify({"error": "Unauthorized"}), 401

    student = Student.query.filter_by(user_id=session['user_id']).first()

    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.eligible_year == student.year,
        PlacementDrive.eligible_branch == student.branch,
    ).all()
    result = []

    for drive in drives:

        existing = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()

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
            "isEligible": (student.cgpa >= drive.eligible_cgpa),
            "is_applied": True if existing else False
        })

    return jsonify(result)

@student_bp.route('/student/apply/<int:drive_id>', methods=['POST'])
def apply_drive(drive_id):

    if 'user_id' not in session or session.get('role') != 'student':
        return jsonify({"error": "Unauthorized"}), 401

    student = Student.query.filter_by(user_id=session['user_id']).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    drive = PlacementDrive.query.get(drive_id)
    if not drive or drive.status != "Approved":
        return jsonify({"error": "Drive not available"}), 404

    if student.cgpa < drive.eligible_cgpa:
        return jsonify({"error": "CGPA criteria not met"}), 403

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    if existing:
        return jsonify({"message": "Already applied"}), 200

    application = Application(
        student_id=student.id,
        drive_id=drive.id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Applied successfully"}), 201

@student_bp.route('/student/applications', methods = ['GET'])
def get_applications():
    if 'user_id' not in session or session.get('role') != 'student':
        return jsonify({"error": "Unauthorized"}), 401
    
    applications = Application.query.filter_by(student_id = session['user_id']).all()
    result = []

    for application in applications:
        result.append({
            "application_id": application.id,
            "drive_id": application.drive.id,
            "company": application.drive.company.name,
            "job_title": application.drive.job_title,
            "status": application.status,
            "applied_at": application.applied_at.strftime("%d-%m-%Y"),
            "feedback": application.feedback if application.feedback else "N.A",
            "interview_date": application.interview_date.strftime("%d-%m-%Y") if application.interview_date else None
        })
    
    return jsonify(result)

@student_bp.route('/student/profile', methods=['POST'])
def update_profile():

    if 'user_id' not in session or session.get('role') != 'student':
        return jsonify({"error": "Unauthorized"}), 401

    student = Student.query.filter_by(user_id=session['user_id']).first()

    student.roll_number = request.form.get('roll_number', student.roll_number)
    student.phone = request.form.get('phone', student.phone)
    student.skills = request.form.get('skills', student.skills)
    student.bio = request.form.get('bio', student.bio)
    student.cgpa = request.form.get('cgpa', student.cgpa)

    resume = request.files.get('resume')
    if resume:
        resume_filename = f"resume_{student.id}_{resume.filename}"
        resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resume_filename)
        resume.save(resume_path)
        student.resume_path = resume_filename

    profile_pic = request.files.get('profile_pic')
    if profile_pic:
        pic_filename = f"profile_{student.id}_{profile_pic.filename}"
        pic_path = os.path.join(current_app.config['UPLOAD_FOLDER'], pic_filename)
        profile_pic.save(pic_path)
        student.profile_pic = pic_filename

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})

@student_bp.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)