"""
Student Forms

WTForms for student management (add, edit).

What is WTForms?
- Python form library for Flask
- Handles form validation
- Generates HTML forms
- Prevents common security issues (CSRF, XSS)

Why use WTForms?
- Server-side validation (secure)
- Consistent validation rules
- Easy to render in templates
- Built-in CSRF protection
"""

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, Email, ValidationError
from datetime import date


class StudentForm(FlaskForm):
    """
    Form for adding a new student
    
    This form validates all student input before saving to database.
    """
    
    # Name fields
    first_name = StringField(
        'First Name',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Enter first name'}
    )
    
    last_name = StringField(
        'Last Name',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Enter last name'}
    )
    
    father_name = StringField(
        'Father Name',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Enter father name'}
    )
    
    # Date of birth
    date_of_birth = DateField(
        'Date of Birth',
        validators=[DataRequired()],
        default=date.today
    )
    
    # Gender selection
    gender = SelectField(
        'Gender',
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        validators=[DataRequired()]
    )
    
    # Class selection (will be populated dynamically)
    class_grade_id = SelectField(
        'Class/Grade',
        coerce=int,  # Convert to integer
        validators=[Optional()],
        choices=[]  # Will be populated in view
    )
    
    # Admission details
    admission_date = DateField(
        'Admission Date',
        validators=[DataRequired()],
        default=date.today
    )
    
    # Note: admission_number is auto-generated, not in form
    
    address = TextAreaField(
        'Address',
        validators=[Optional()],
        render_kw={'rows': 3, 'placeholder': 'Enter address'}
    )
    
    # Parent/Guardian information
    parent_guardian_name = StringField(
        'Parent/Guardian Name',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Enter parent/guardian name'}
    )
    
    parent_primary_contact = StringField(
        'Primary Contact Number',
        validators=[DataRequired(), Length(max=20)],
        render_kw={'placeholder': '+92-300-1234567'}
    )
    
    parent_secondary_contact = StringField(
        'Secondary Contact Number (Optional)',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': '+92-300-1234567'}
    )
    
    # Family selection - improved with "has siblings" option
    has_siblings = SelectField(
        'Does this student have siblings in school?',
        choices=[('no', 'No'), ('yes', 'Yes')],
        validators=[DataRequired()],
        default='no'
    )
    
    family_id = SelectField(
        'Select Family (if siblings exist)',
        coerce=int,
        validators=[Optional()],
        choices=[(0, '-- No Family --')]  # Will be populated in view
    )
    
    # Active status - default to Active
    is_active = SelectField(
        'Status',
        choices=[(True, 'Active'), (False, 'Inactive')],
        coerce=lambda x: x == 'True',
        default=True
    )
    
    def validate_date_of_birth(self, field):
        """
        Custom validator: Date of birth should be in the past
        """
        if field.data and field.data > date.today():
            raise ValidationError('Date of birth cannot be in the future.')
    
    def validate_admission_date(self, field):
        """
        Custom validator: Admission date should be reasonable
        """
        if field.data and field.data > date.today():
            raise ValidationError('Admission date cannot be in the future.')
    
    def validate_family_id(self, field):
        """
        Custom validator: If has_siblings is 'yes', family_id must be selected
        """
        if self.has_siblings.data == 'yes' and (not field.data or field.data == 0):
            raise ValidationError('Please select a family if student has siblings in school.')


class StudentEditForm(StudentForm):
    """
    Form for editing an existing student
    
    Inherits from StudentForm but allows admission number to remain the same.
    """
    
    def __init__(self, student=None, *args, **kwargs):
        """
        Initialize form with existing student data
        
        Parameters:
        student: The student being edited (to exclude from uniqueness check)
        """
        super(StudentEditForm, self).__init__(*args, **kwargs)
        self.student = student
    
    # Note: admission_number is auto-generated, no validation needed
