"""
Forms Package

This package contains all WTForms form classes.
WTForms handles form validation and rendering.

Why separate forms?
- Clean separation of concerns
- Reusable form classes
- Easy to test validation logic
- Consistent validation across the app
"""

from app.forms.student_forms import StudentForm, StudentEditForm
from app.forms.family_forms import FamilyForm, FamilyEditForm

__all__ = [
    'StudentForm',
    'StudentEditForm',
    'FamilyForm',
    'FamilyEditForm'
]
