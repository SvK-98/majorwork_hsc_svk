import os
import sys
import threading
import platform
import webview
import logging
from werkzeug.serving import make_server

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SukeshEducationDesktop')

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import our Flask app
from sukesh_education.app import create_app, db
from sukesh_education.app.models import User

# API class for JavaScript interaction
class WindowAPI:
    def __init__(self, window):
        self.window = window
    
    def minimize_window(self):
        """Minimize the window"""
        logger.info("Minimizing window")
        self.window.minimize()
        return True
    
    def get_system_info(self):
        """Get system information"""
        return {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "pywebview_version": webview.__version__,
            "processor": platform.processor()
        }

class ServerThread(threading.Thread):
    def __init__(self, app, host='127.0.0.1', port=0):
        """
        Initialize the server thread with Flask app
        
        Args:
            app: The Flask application instance
            host: Host to bind the server to
            port: Port to bind the server to, 0 means any available port
        """
        threading.Thread.__init__(self, daemon=True)
        self.name = "FlaskServerThread"
        
        self.host = host
        self.port = port
        self.app = app
        
        # Create WSGI server
        self.server = make_server(self.host, self.port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        
        # Get the port that was assigned
        self.port = self.server.socket.getsockname()[1]
        logger.info(f"Flask server will run on {self.host}:{self.port}")
        
    def run(self):
        """Run the server"""
        logger.info("Starting Flask server")
        self.server.serve_forever()
        
    def shutdown(self):
        """Shutdown the server"""
        logger.info("Shutting down Flask server")
        self.server.shutdown()
        
def create_test_user(app):
    """Create a test user if it doesn't exist"""
    try:
        with app.app_context():
            # Create tables if they don't exist
            db.create_all()
            
            # Check if we need to create a test user
            if not User.query.filter_by(email='test@example.com').first():
                user = User(email='test@example.com', name='Test User')
                user.set_password('password123')
                db.session.add(user)
                db.session.commit()
                logger.info('Test user created with email: test@example.com and password: password123')
            else:
                logger.info('Test user already exists')
    except Exception as e:
        logger.error(f"Error creating test user: {str(e)}")
        raise

def get_gui_type():
    """Determine the best GUI toolkit to use based on OS"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return "cocoa"
    elif system == "Windows":
        # Try to use Edge/Chromium if available, otherwise try other renderers
        if webview.platforms.edgechromium.EdgeChrome.is_available():
            return "edgechromium"
        elif webview.platforms.cef.CEF.is_available():
            return "cef"
        else:
            return None
    elif system == "Linux":
        # Try GTK first, then Qt
        if webview.platforms.gtk.is_gtk_available():
            return "gtk"
        elif hasattr(webview.platforms, 'qt') and hasattr(webview.platforms.qt, 'is_qt_available') and webview.platforms.qt.is_qt_available():
            return "qt"
        else:
            return None
    
    return None  # Default will be chosen by pywebview

def main():
    try:
        # Create Flask app
        logger.info("Initializing Flask application")
        app = create_app()
        
        # Create test user
        create_test_user(app)
        
        # Start Flask server in a separate thread
        logger.info("Starting server thread")
        server = ServerThread(app)
        server.start()
        
        # Get the server URL
        url = f"http://127.0.0.1:{server.port}"
        logger.info(f"Server running at {url}")
        
        # Validate and log the URL
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError(f"Invalid URL format: {url}")
        logger.debug(f"Validated URL: {url}")
        
        # Determine best GUI toolkit
        gui_type = get_gui_type()
        logger.info(f"Using GUI toolkit: {gui_type or 'default'}")
        
        # Window customizations
        window_settings = {
            'title': 'Sukesh Education',
            'width': 1200,
            'height': 800,
            'resizable': True,
            'min_size': (800, 600),
            'background_color': '#f5f7fa',
            'text_select': True,
            'frameless': False,
            'easy_drag': True,
            'zoomable': True,
        }
        
        # Create desktop window with Flask app
        logger.info("Creating window")
        # Remove title from window_settings since we pass it directly
        window_title = window_settings.pop('title')
        
        # Log the exact URL being passed to webview.create_window
        logger.info(f"Passing URL to webview.create_window: {url}")
        
        window = webview.create_window(window_title, url, **window_settings)
        
        # Create and expose API to JavaScript
        api = WindowAPI(window)
        window.expose(api)
        
        # Start the desktop application
        logger.info("Starting desktop application")
        webview.start(debug=True, gui=gui_type)
        
        # Clean up server when closing
        logger.info("Application closed, shutting down server")
        server.shutdown()
        
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}")
        # Display error in a window if possible
        try:
            webview.create_window('Error', f"<html><body><h2>Error starting Sukesh Education</h2><p>{str(e)}</p></body></html>", width=500, height=300)
            webview.start()
        except:
            print(f"Error: {str(e)}")
        return 1
    
    return 0
    
if __name__ == '__main__':
    sys.exit(main())
