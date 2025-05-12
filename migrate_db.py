import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sukesh_education.app import create_app, db
from sukesh_education.app.models import User

def recreate_database():
    """Drop all tables and recreate them"""
    print("Starting database migration...")
    app = create_app()
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables with updated schema...")
        db.create_all()
        
        # Create test user
        print("Creating test user...")
        user = User(email='test@example.com', name='Test User')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        print("Database migration completed successfully.")

if __name__ == "__main__":
    recreate_database()
