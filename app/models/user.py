"""
User Model

This represents the admin/user table in the database.
Since we only have one admin, this is a simple user model.

What is a Model?
- A Python class that represents a database table
- Each instance = one row in the table
- Attributes = columns in the table
"""

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    """
    User Model (Admin)
    
    This table stores admin user information.
    UserMixin provides methods like is_authenticated, is_active, etc.
    
    Table name: user
    """
    
    # Table name (optional - SQLAlchemy uses class name by default)
    __tablename__ = 'user'
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key: Unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # Username: Must be unique, required
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Email: Optional, can be used for password reset later
    email = db.Column(db.String(100), nullable=True)
    
    # Password Hash: We NEVER store plain passwords!
    # We store a hash (encrypted version) for security
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Active Status: Can deactivate user without deleting
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps: Track when user was created/updated
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ========== METHODS ==========
    
    def set_password(self, password):
        """
        Set user password
        
        We hash the password before storing it.
        This is a security best practice - never store plain passwords!
        
        Parameters:
        password: Plain text password from user input
        """
        # generate_password_hash creates a secure hash
        # It includes salt (random data) to prevent rainbow table attacks
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if provided password matches stored hash
        
        We compare the hash of the input password with the stored hash.
        
        Parameters:
        password: Plain text password to check
        
        Returns:
        True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """
        String representation of the object
        
        Useful for debugging and logging.
        Example: <User admin>
        """
        return f'<User {self.username}>'
