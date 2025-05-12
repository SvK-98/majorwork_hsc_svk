import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sukesh_education.app import create_app, db
from sukesh_education.app.models import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Provide objects for the flask shell context"""
    return {'db': db, 'User': User}

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if we need to create a test user
        if not User.query.filter_by(email='test@example.com').first():
            user = User(email='test@example.com', name='Test User')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            print('Test user created with email: test@example.com and password: password123')
        
    app.run(debug=True)
