from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, Regexp
from flask_login import current_user
from werkzeug.security import check_password_hash

# Fix import path to match the project structure
from sukesh_education.app.models import User

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Enter a valid email address'),
        Length(max=120)
    ])
    name = StringField('Name', validators=[
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        """Check if email is already registered"""
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class ForgotPasswordForm(FlaskForm):
    """Form for password reset request"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Enter a valid email address')
    ])
    submit = SubmitField('Reset Password')

class UpdateProfileForm(FlaskForm):
    """Form for updating user profile"""
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=200)])
    phone_number = StringField('Phone Number', validators=[
        Optional(), 
        Length(max=20),
        Regexp(r'^\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$', 
               message="Invalid phone number format. Use a valid format like +1 (123) 456-7890 or 123-456-7890.")
    ])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Changes')

class ChangePasswordForm(FlaskForm):
    """Form for changing user password"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), 
        EqualTo('new_password', message='New passwords must match.')
    ])
    submit_password = SubmitField('Change Password')

    def validate_current_password(self, field):
        """Validate that the current password is correct."""
        if not current_user.is_authenticated or not check_password_hash(current_user.password_hash, field.data):
            raise ValidationError('Incorrect current password.')
