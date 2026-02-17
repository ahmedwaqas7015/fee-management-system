"""
Application Entry Point

This is the main file you run to start the Flask application.
Run it with: python run.py

Why separate from app/__init__.py?
- Keeps the factory function clean
- Makes it clear where to start the app
- Allows easy configuration changes
"""

from app import create_app, db
from app.models import User  # We'll create this model next
from flask_migrate import upgrade

# Create the Flask application
# 'development' means we're using DevelopmentConfig from config.py
app = create_app('development')


@app.shell_context_processor
def make_shell_context():
    """
    Shell Context Processor
    
    This makes certain objects available in Flask shell.
    Useful for testing and database operations.
    
    Run: flask shell
    Then you can use: db, User, Student, etc. directly
    """
    return {
        'db': db,
        'User': User,
        # We'll add more models here as we create them
    }


@app.cli.command('init-db')
def init_db():
    """
    Custom Flask CLI command to initialize database
    
    Run with: flask init-db
    OR: FLASK_APP=run.py flask init-db
    
    This creates all database tables and creates an admin user.
    """
    print("Creating database tables...")
    db.create_all()
    print("Database tables created!")
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@school.com'
        )
        admin.set_password('admin123')  # Change this in production!
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
        print("Username: admin")
        print("Password: admin123")
        print("⚠️  IMPORTANT: Change the password after first login!")
    else:
        print("Admin user already exists.")


# Alternative: Python function that can be called directly
def init_database():
    """
    Initialize database - can be called directly from Python
    
    Usage: python -c "from run import init_database; init_database()"
    """
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created!")
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@school.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
            print("Username: admin")
            print("Password: admin123")
            print("⚠️  IMPORTANT: Change the password after first login!")
        else:
            print("Admin user already exists.")


if __name__ == '__main__':
    """
    This runs when you execute: python run.py
    
    It starts the Flask development server.
    """
    # Run the Flask development server
    # debug=True enables auto-reload on code changes
    # host='127.0.0.1' means only accessible from localhost
    # port=5000 is the default Flask port
    app.run(debug=True, host='127.0.0.1', port=5000)
