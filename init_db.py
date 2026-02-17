"""
Database Initialization Script

This script initializes the database and creates the admin user.
You can run it directly: python init_db.py

This is an alternative to using 'flask init-db' command.

Note: With Flask-Migrate, we use migrations instead of db.create_all()
But this script still works for creating the admin user.
"""

from app import create_app, db
from app.models import User

# Create the Flask application
app = create_app('development')

def init_database():
    """
    Initialize database and create admin user
    
    Note: Database tables are created via migrations (flask db upgrade)
    This function only creates the admin user if it doesn't exist.
    """
    with app.app_context():
        print("=" * 50)
        print("Initializing Fee Management System Database")
        print("=" * 50)
        
        print("\n1. Checking database tables...")
        print("   (Tables should be created via migrations: flask db upgrade)")
        
        print("\n2. Checking for admin user...")
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("   Creating admin user...")
            admin = User(
                username='admin',
                email='admin@school.com'
            )
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print("   ✅ Admin user created!")
            print("\n" + "=" * 50)
            print("Default Login Credentials:")
            print("=" * 50)
            print("   Username: admin")
            print("   Password: admin123")
            print("\n⚠️  IMPORTANT: Change the password after first login!")
            print("=" * 50)
        else:
            print("   ✅ Admin user already exists.")
            print("\n" + "=" * 50)
            print("Database initialization complete!")
            print("=" * 50)

if __name__ == '__main__':
    init_database()
