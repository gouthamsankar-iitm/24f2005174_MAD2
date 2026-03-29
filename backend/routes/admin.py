from flask import Blueprint, request, jsonify, session
from models import db, User, Company, Student, PlacementDrive

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/companies/pending', methods=['GET'])
def get_pending_companies():
    companies = Company.query.filter_by(approval_status = "Pending").all()

    result = []
    for company in companies:
        result.append({
        "id": company.id,
        "name": company.name,
        "email": company.user.email,
        "hr_contact": company.hr_contact,
        "website": company.website,
        "industry": company.industry,
        "location": company.location,
        "status": company.approval_status,
        "registered_at": company.registered_at
    })
        
    return jsonify(result)

@admin_bp.route('/admin/companies/pending/count', methods=['GET'])
def get_pending_count():
    count = Company.query.filter_by(approval_status="Pending").count()
    return jsonify({"count": count})

@admin_bp.route('/admin/company/<int:id>/approve', methods = ['POST'])
def company_approve(id):

    company = Company.query.get(id) #? ?
    company.approval_status = "Approved"
    db.session.commit()

    return jsonify({"message": "Comapny approved"})

@admin_bp.route('/admin/company/<int:id>/reject', methods = ['POST'])
def company_reject(id):

    company = Company.query.get(id) 
    company.approval_status = "Rejected"
    db.session.commit()

    return jsonify({"message": "Comapny rejected"})

@admin_bp.route('/admin/drives/pending', methods=['GET'])
def get_pending_drives():

    drives = PlacementDrive.query.filter_by(status="Pending").all()

    result = []
    for drive in drives:
        result.append({
            "id": drive.id,
            "company": drive.company.name,  
            "job_title": drive.job_title,
            "job_type": drive.job_type,
            "location": drive.location,
            "package": drive.package,
            "eligible_branch": drive.eligible_branch,
            "eligible_cgpa": drive.eligible_cgpa,
            "eligible_year": drive.eligible_year,
            "vacancy": drive.vacancy,
            "rounds": drive.rounds,
            "deadline": drive.deadline,
            "status": drive.status,
        })

    return jsonify(result)

@admin_bp.route('/admin/drive/<int:id>/approve', methods=['POST'])
def drive_approve(id):
    drive = PlacementDrive.query.get(id)
    drive.status = "Approved"
    db.session.commit()

    return jsonify({"message": "Drive approved"})

@admin_bp.route('/admin/drive/<int:id>/reject', methods=['POST'])
def drive_reject(id):
    drive = PlacementDrive.query.get(id)
    drive.status = "Rejected"
    db.session.commit()

    return jsonify({"message": "Drive rejected"})