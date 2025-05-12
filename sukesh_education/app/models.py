from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile and educational information
    year_level = db.Column(db.String(20), nullable=True)  # Year 11 or Year 12
    hsc_subjects = db.Column(db.String(500), nullable=True)  # Comma-separated list of subjects
    
    def __init__(self, email, name=None, year_level=None, hsc_subjects=None):
        self.email = email
        self.name = name
        self.year_level = year_level
        self.hsc_subjects = hsc_subjects
    
    def set_password(self, password):
        """Hash the password for storage"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'
