from flask import Blueprint, request, jsonify, session
from models import db, Company, PlacementDrive
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