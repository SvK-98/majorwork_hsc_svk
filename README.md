# Sukesh Education - Desktop Authentication System

A beautiful desktop authentication system for Sukesh Education built with Flask, SQLAlchemy, Bootstrap 5, and PyWebView.

## Features

- User authentication (login, registration, logout)
- Password hashing for security
- Responsive design with Bootstrap 5
- Clean and modern UI with custom branding
- Form validation
- Flash messages for user feedback
- Native desktop application experience with PyWebView
- Cross-platform compatibility (Windows, macOS, Linux)

## Tech Stack

- **Backend**: Python 3.9+ with Flask
- **Database**: SQLite for development
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login + Werkzeug password hashing
- **Forms**: Flask-WTF with validation
- **Frontend**: Bootstrap 5 with custom styles
- **Icons**: Bootstrap Icons
- **Desktop Framework**: PyWebView
- **Threading**: Python's threading module for running Flask in the background

## Project Structure

```
├── desktop.py           # Desktop application entry point
├── run_desktop.sh       # Shell script to run the desktop app
├── requirements.txt     # Python dependencies
├── instance/            # Database files
│   └── education.db     # SQLite database
├── sukesh_education/
│   ├── app/
│   │   ├── __init__.py       # Flask application factory
│   │   ├── models.py         # Database models
│   │   ├── auth/             # Authentication blueprint
│   │   │   ├── views.py      # Auth routes
│   │   │   └── forms.py      # Auth forms
│   │   ├── static/           # Static assets
│   │   │   ├── css/          # CSS files
│   │   │   ├── js/           # JavaScript files
│   │   │   └── images/       # Images and icons
│   │   └── templates/        # Jinja2 templates
│   │       ├── base.html     # Base template
│   │       ├── index.html    # Home page
│   │       └── auth/         # Auth templates
│   │           ├── login.html
│   │           ├── register.html
│   │           └── forgot_password.html
│   ├── config.py        # Configuration settings
│   └── run.py           # Web application entry point
```

## Installation

1. Clone the repository
   
2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Desktop Application (Recommended)

1. Run the desktop application:
   ```bash
   ./run_desktop.sh  # On Windows: run_desktop.bat
   ```
   
   Or using Python directly:
   ```bash
   python desktop.py
   ```

2. The application will open in a desktop window

### Web Application (Alternative)

1. Run the web application:
   ```bash
   python sukesh_education/run.py
   ```

2. Access the application at http://127.0.0.1:5000/

## Default User

The application comes with a test user:
- Email: `test@example.com`
- Password: `password123`

## Branding

The color palette for Sukesh Education:
- Primary: #4361ee (Deep Blue)
- Secondary: #7209b7 (Purple)
- Accent: #f72585 (Bright Pink)

## Security Features

- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Secure session cookies

## Future Enhancements

- Email confirmation
- Password reset functionality
- Social login options
- User profile management
- Admin dashboard
