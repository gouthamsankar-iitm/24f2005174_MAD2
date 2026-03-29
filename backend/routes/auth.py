from flask import Blueprint, request, jsonify, session
from models import db, User, Company, Student

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods = ['POST'])
def login():

    data = request.json
    user = User.query.filter_by(email = data['email']).first()

    if not user:
        return jsonify({"error": "Account not found. Please sign up."}), 404
    
    if(user.password != data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    if(user.role == 'company'):
        comapny = Company.query.filter_by(user_id = user.id).first()
        if(comapny.approval_status != "Approved"):
            return jsonify({"error": "Please wait till your company is approved."}), 403

    
    session['user_id'] = user.id
    session['role'] = user.role

    return jsonify({
        "message": "Login successful",
        "role": user.role
    })

@auth_bp.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully."})

@auth_bp.route('/signup/student', methods = ['POST'])
def student_signup():
    data = request.json

    user = User(
        email = data['email'],
        password = data['password'],
        role ='student'
    )
    db.session.add(user)
    db.session.commit()

    student = Student(
        user_id=user.id,
        name = data['name'],
        branch = data['branch'],
        cgpa = data['cgpa'],
        year = data['year']
    )
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered"}), 201

@auth_bp.route('/signup/company', methods=['POST'])
def company_signup():
    data = request.json

    user = User(
        email=data['email'],
        password=data['password'],
        role='company'
    )
    db.session.add(user)
    db.session.commit()

    company = Company(
        user_id=user.id,
        name=data['name'],
        hr_contact=data['hr_contact'],
        website=data['website'],
        approval_status='Pending'
    )
    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Company registered, waiting for approval"}), 201