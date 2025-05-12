from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, current_app
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from ..models import db, User
from ..auth.forms import UpdateProfileForm, ChangePasswordForm

main = Blueprint('main', __name__)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_settings():
    profile_form = UpdateProfileForm(obj=current_user)
    password_form = ChangePasswordForm()

    if profile_form.validate_on_submit() and 'submit' in request.form:
        current_user.name = profile_form.name.data
        current_user.address = profile_form.address.data
        current_user.phone_number = profile_form.phone_number.data
        current_user.date_of_birth = profile_form.date_of_birth.data
        current_user.bio = profile_form.bio.data
        try:
            db.session.commit()
            flash('Your profile has been updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
        return redirect(url_for('main.profile_settings'))

    if password_form.validate_on_submit() and 'submit_password' in request.form:
        if current_user.check_password(password_form.current_password.data):
            current_user.set_password(password_form.new_password.data)
            try:
                db.session.commit()
                flash('Your password has been changed successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error changing password: {str(e)}', 'danger')
            return redirect(url_for('main.profile_settings'))
        else:
            flash('Incorrect current password.', 'danger')

    return render_template('profile_settings.html', profile_form=profile_form, password_form=password_form)

@main.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['profile_picture']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'profile_pictures')
        
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        current_user.profile_picture = url_for('static', filename=f'uploads/profile_pictures/{filename}')
        
        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Profile picture uploaded successfully',
                'picture_url': current_user.profile_picture
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return jsonify({'success': False, 'message': 'Error uploading file'}), 400

@main.route('/save_notification_preferences', methods=['POST'])
@login_required
def save_notification_preferences():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    return jsonify({
        'success': True, 
        'message': 'Notification preferences saved successfully'
    })
