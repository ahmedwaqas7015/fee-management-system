"""
Family Forms

WTForms for family management (add, edit).

Families group siblings together for group payments.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
import re


class FamilyForm(FlaskForm):
    """
    Form for adding a new family
    
    Used when creating a family to group siblings.
    """
    
    father_name = StringField(
        'Father Name',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Enter father name'}
    )
    
    father_cnic = StringField(
        'Father CNIC',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': 'XXXXX-XXXXXXX-X'}
    )
    
    father_contact = StringField(
        'Father Contact',
        validators=[DataRequired(), Length(max=20)],
        render_kw={'placeholder': '+92-300-1234567'}
    )
    
    mother_name = StringField(
        'Mother Name',
        validators=[Optional(), Length(max=100)],
        render_kw={'placeholder': 'Enter mother name (optional)'}
    )
    
    address = TextAreaField(
        'Address',
        validators=[Optional()],
        render_kw={'rows': 3, 'placeholder': 'Enter family address'}
    )
    
    def validate_father_cnic(self, field):
        """
        Custom validator: Validate Pakistani CNIC format
        
        Format: XXXXX-XXXXXXX-X
        Example: 12345-1234567-1
        """
        if field.data:
            pattern = r'^\d{5}-\d{7}-\d{1}$'
            if not re.match(pattern, field.data):
                raise ValidationError('CNIC must be in format: XXXXX-XXXXXXX-X')
    
    def validate_father_cnic_unique(self):
        """
        Check if CNIC is unique (if provided)
        """
        from app.models import Family
        
        if self.father_cnic.data:
            existing = Family.query.filter_by(father_cnic=self.father_cnic.data).first()
            if existing:
                raise ValidationError('This CNIC is already registered with another family.')


class FamilyEditForm(FamilyForm):
    """
    Form for editing an existing family
    """
    
    def __init__(self, family=None, *args, **kwargs):
        super(FamilyEditForm, self).__init__(*args, **kwargs)
        self.family = family
    
    def validate_father_cnic_unique(self):
        """
        Check uniqueness, but allow current family's CNIC
        """
        from app.models import Family
        
        if self.father_cnic.data:
            query = Family.query.filter_by(father_cnic=self.father_cnic.data)
            if self.family:
                query = query.filter(Family.id != self.family.id)
            
            existing = query.first()
            if existing:
                raise ValidationError('This CNIC is already registered with another family.')
