"""
Flask Application Factory

This is the main entry point for creating the Flask application.
We use the "Application Factory" pattern which is a best practice.

Why Application Factory?
- Allows creating multiple app instances (useful for testing)
- Better organization and modularity
- Easier to configure for different environments
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from config import config
import os
import logging
from logging.handlers import RotatingFileHandler

# Get base directory for translations (go up one level from app/ to project root)
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Initialize extensions (but don't attach to app yet)
# This is important - we initialize them here but configure them in create_app()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
babel = Babel()
csrf = CSRFProtect()


def create_app(config_name='default'):
    """
    Application Factory Function
    
    This function creates and configures the Flask application.
    It's called the "factory pattern" because it "manufactures" app instances.
    
    Parameters:
    config_name: Which configuration to use ('development', 'production', 'testing')
    
    Returns:
    Configured Flask application instance
    """
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    # This loads settings from config.py based on the environment
    app.config.from_object(config[config_name])
    
    # Ensure instance folder exists (for SQLite database)
    # The 'instance' folder is Flask's convention for app-specific files
    instance_path = app.instance_path
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    # Ensure media and logs directories exist
    # These folders will store uploaded files and log files
    for folder in ['media', 'logs', 'backups']:
        folder_path = os.path.join(app.root_path, '..', folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # Set Babel translation directories BEFORE initializing Babel
    # This tells Flask-Babel where to find translation files
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(basedir, 'translations')
    
    # ========== FLASK-BABEL CONFIGURATION ==========
    # Configure language selection
    # In Flask-Babel 4.0, locale_selector is passed as a parameter to init_app()
    # This function determines which language to use
    def get_locale():
        """
        Determine the locale (language) to use
        
        This checks:
        1. Language in session (user's choice)
        2. Accept-Language header (browser preference)
        3. Default language from config
        """
        from flask import session, request
        
        # Check if user has selected a language
        if 'language' in session:
            lang = session['language']
            if lang in app.config['LANGUAGES'].keys():
                return lang
        
        # Otherwise, use browser's preferred language or default
        return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or app.config['BABEL_DEFAULT_LOCALE']
    
    # Initialize extensions with the app
    # Now we attach all our extensions to the Flask app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    # Pass locale_selector to init_app() in Flask-Babel 4.0
    babel.init_app(app, locale_selector=get_locale)
    csrf.init_app(app)
    
    # Ensure locale is refreshed on each request
    # This clears any cached locale so get_locale() is called fresh
    @app.before_request
    def clear_babel_cache():
        """Clear Babel locale cache before each request to ensure fresh locale selection"""
        from flask import g
        # Clear any cached Babel locale
        if hasattr(g, '_babel_locale'):
            delattr(g, '_babel_locale')
        if hasattr(g, '_babel'):
            # Clear the entire Babel cache if it exists
            if hasattr(g._babel, '_locale'):
                delattr(g._babel, '_locale')
    
    # ========== FLASK-LOGIN CONFIGURATION ==========
    # Configure Flask-Login for authentication
    
    # Set the login view (where users go if not logged in)
    login_manager.login_view = 'auth.login'
    
    # Set the message category for flash messages
    login_manager.login_message_category = 'info'
    
    # Set session protection (strong = logout on IP change)
    login_manager.session_protection = 'strong'
    
    # ========== LOGGING CONFIGURATION ==========
    # Set up logging for the application
    # Logs help us debug issues and track what's happening
    if not app.debug:  # Only log to file in production
        if not os.path.exists(app.config['LOG_DIR']):
            os.makedirs(app.config['LOG_DIR'])
        
        # Create rotating file handler
        # This automatically creates new log files when current one gets too big
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=app.config['LOG_FILE_MAX_SIZE'],
            backupCount=app.config['LOG_BACKUP_COUNT']
        )
        
        # Set log format
        # Format: Timestamp | Level | Module | Function | Line | Message
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(lineno)d | %(message)s'
        ))
        
        # Set log level (INFO = normal operations, ERROR = errors only)
        file_handler.setLevel(logging.INFO)
        
        # Add handler to Flask's logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Fee Management System startup')
    
    # ========== REGISTER BLUEPRINTS ==========
    # Blueprints are Flask's way of organizing routes
    # We'll create these in separate files for better organization
    
    # Register authentication routes (login, logout, etc.)
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Register main routes (dashboard, students, etc.)
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Register student management routes
    from app.routes.students import bp as students_bp
    app.register_blueprint(students_bp)
    
    # Register family management routes
    from app.routes.families import bp as families_bp
    app.register_blueprint(families_bp)
    
    # ========== LOGIN MANAGER USER LOADER ==========
    # This tells Flask-Login how to find a user by ID
    # We need to import User here to avoid circular imports
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Load user by ID
        
        Flask-Login calls this function to get the user object
        when it needs to check if a user is logged in.
        
        Parameters:
        user_id: The user's ID (from session)
        
        Returns:
        User object or None if not found
        """
        return User.query.get(int(user_id))
    
    # ========== ERROR HANDLERS ==========
    # Custom error pages for better user experience
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors"""
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors"""
        from flask import render_template
        db.session.rollback()  # Rollback any failed database transaction
        return render_template('errors/500.html'), 500
    
    # ========== CONTEXT PROCESSORS ==========
    # These make variables available to all templates
    # Useful for things like current user, language, etc.
    
    @app.context_processor
    def inject_user():
        """Make current_user available in all templates"""
        from flask_login import current_user
        return dict(current_user=current_user)
    
    @app.context_processor
    def inject_language():
        """Make current language available in all templates"""
        # Use Flask-Babel's get_locale() to ensure consistency
        from flask_babel import get_locale
        current_lang = get_locale()
        return dict(current_language=current_lang)
    
    # Return the configured app
    return app
