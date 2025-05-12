<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Sukesh Education - Authentication System

This is a Flask-based authentication system for Sukesh Education with the following features:

- Python Flask backend with SQLAlchemy ORM
- User authentication (login, registration, logout)
- Password hashing with Werkzeug
- Form validation with Flask-WTF
- Bootstrap 5 for responsive UI
- Custom styling and branding

## Style Guide

- Use PEP8 standards for Python code
- Follow Flask factory pattern for application creation
- Use Bootstrap 5 classes for UI styling
- Use Sukesh Education's color palette:
  - Primary: #4361ee (Deep Blue)
  - Secondary: #7209b7 (Purple)
  - Accent: #f72585 (Bright Pink)

## Security Practices

- Always use password hashing
- Implement CSRF protection
- Validate form inputs
- Use secure session cookies in production
