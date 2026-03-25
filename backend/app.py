from flask import Flask
from flask_cors import CORS
from models import db, User
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hirestack.db'

CORS(app)
db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)


def create_admin():
    admin = User.query.filter_by(role = 'admin').first()

    if not admin:
        admin = User(
                    email = "hirestack@google.com",
                    password = "Admin@123",
                    role = "admin"
        )
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_admin()


if __name__ == '__main__':
    app.run(debug=True)