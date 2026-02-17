"""
Models Package

This package contains all database models (tables).
We organize models into separate files for better maintainability.

Models are SQLAlchemy classes that represent database tables.
Each model class = one database table.

IMPORTANT: Import order matters!
- Base models first (no dependencies)
- Then models that depend on base models
- This prevents circular import issues
"""

from app import db

# Import all models
# Order matters: import base models first, then dependent models

# Base models (no dependencies)
from app.models.user import User
from app.models.class_grade import ClassGrade
from app.models.academic_year import AcademicYear
from app.models.family import Family

# Models that depend on base models
from app.models.student import Student
from app.models.fee_structure import FeeStructure, fee_structure_classes
from app.models.fee_payment import FeePayment
from app.models.group_payment import GroupPayment
from app.models.payment_receipt import PaymentReceipt

# Export all models
# This ensures all tables are registered with SQLAlchemy
# When we run db.create_all(), all these tables will be created

__all__ = [
    'User',
    'ClassGrade',
    'AcademicYear',
    'Family',
    'Student',
    'FeeStructure',
    'fee_structure_classes',  # Junction table
    'FeePayment',
    'GroupPayment',
    'PaymentReceipt'
]
