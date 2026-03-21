from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .student import Student
from .company import Company
from .drive import PlacementDrive
from .application import Application