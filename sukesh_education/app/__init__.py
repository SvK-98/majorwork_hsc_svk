import os
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from .models import db, User
from sukesh_education.config import config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_name=None):
    """Factory pattern to create Flask app with configuration"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)
    migrate.init_app(app, db)
    
    # Configure CSRF protection
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = app.config['SECRET_KEY']
    
    # Register blueprints
    from .auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/save-profile', methods=['POST'])
    @login_required
    def save_profile():
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        try:
            year_level = data.get('year_level')
            hsc_subjects = data.get('hsc_subjects')
            
            if not year_level:
                return jsonify({'success': False, 'message': 'Year level is required'}), 400
                
            current_user.year_level = year_level
            current_user.hsc_subjects = hsc_subjects
            
            db.session.add(current_user)
            db.session.commit()
            
            app.logger.info(f"Updated profile for user {current_user.email}: Year={year_level}, Subjects={hsc_subjects}")
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error saving profile: {str(e)}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return app
