"""
Authentication Routes

This blueprint handles login, logout, and authentication-related routes.

What is a Blueprint?
- A way to organize routes into modules
- Like a mini-application within the main app
- Makes code more organized and maintainable
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from flask_babel import gettext as _

# Create blueprint
# 'auth' is the blueprint name
# __name__ tells Flask where the blueprint is defined
bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login Route
    
    GET: Show login form
    POST: Process login form submission
    
    URL: /auth/login
    """
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        # Validate input
        if not username or not password:
            flash(_('Please enter both username and password.'), 'error')
            return render_template('auth/login.html')
        
        # Find user in database
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Check if user is active
            if not user.is_active:
                flash(_('Your account is deactivated. Please contact administrator.'), 'error')
                return render_template('auth/login.html')
            
            # Log the user in
            # login_user is from Flask-Login
            login_user(user, remember=remember)
            
            # Flash success message
            flash(_('Login successful! Welcome back.'), 'success')
            
            # Redirect to dashboard
            # We'll create the dashboard route later
            return redirect(url_for('main.dashboard'))
        else:
            # Invalid credentials
            flash(_('Invalid username or password.'), 'error')
    
    # Show login form (GET request)
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required  # User must be logged in to logout
def logout():
    """
    Logout Route
    
    Logs out the current user and redirects to login page.
    
    URL: /auth/logout
    """
    logout_user()
    flash(_('You have been logged out successfully.'), 'info')
    return redirect(url_for('auth.login'))


@bp.route('/change-language/<language>')
def change_language(language):
    """
    Change Language Route
    
    Allows user to switch between Urdu and English.
    
    URL: /auth/change-language/<language>
    Parameters:
    language: 'ur' for Urdu, 'en' for English
    """
    # Validate language
    if language in ['ur', 'en']:
        session['language'] = language
        flash(_('Language changed successfully.'), 'success')
    else:
        flash(_('Invalid language selection.'), 'error')
    
    # Redirect back to previous page
    # request.referrer is the page user came from
    return redirect(request.referrer or url_for('main.dashboard'))
