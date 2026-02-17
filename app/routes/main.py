"""
Main Routes

This blueprint handles the main application routes like dashboard.

We'll add more routes here as we build the application.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from flask_babel import gettext as _

# Create blueprint
bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required  # User must be logged in
def dashboard():
    """
    Dashboard Route
    
    Main dashboard page showing system overview.
    
    URL: / or /dashboard
    """
    # For now, we'll show a simple dashboard
    # We'll add statistics and charts later
    
    return render_template('main/dashboard.html', title=_('Dashboard'))
