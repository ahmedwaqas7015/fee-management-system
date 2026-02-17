"""
Family Model

This represents a family (group of siblings) for group payment functionality.

Why this model?
- Parents often have multiple children in the same school
- They want to pay all fees together in one payment
- One receipt for all siblings instead of separate receipts
- Better organization and tracking

Example:
- Father: Muhammad Ahmed Khan
- Children: Ahmed (Class 5), Ali (Class 3), Fatima (Class 1)
- All three can pay fees together with one receipt
"""

from app import db
from datetime import datetime
import re


class Family(db.Model):
    """
    Family Model
    
    Groups students who are siblings (brothers/sisters).
    Allows parents to pay fees for all children in a single transaction.
    
    Table name: family
    """
    
    __tablename__ = 'family'
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Family code (unique identifier, auto-generated: FAM-YYYY-XXXX)
    # Format: FAM-2024-0001
    family_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Father's name (primary parent)
    father_name = db.Column(db.String(100), nullable=False)
    
    # Father's CNIC (Computerized National Identity Card)
    # Used for identification and verification
    # Format: XXXXX-XXXXXXX-X (Pakistan CNIC format)
    father_cnic = db.Column(db.String(20), unique=True, nullable=True, index=True)
    
    # Father's contact number (primary contact)
    father_contact = db.Column(db.String(20), nullable=False)
    
    # Mother's name (optional)
    mother_name = db.Column(db.String(100), nullable=True)
    
    # Family address
    address = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ========== RELATIONSHIPS ==========
    # One family can have many students (siblings)
    students = db.relationship('Student', backref='family', lazy='dynamic')
    
    # One family can have many group payments
    group_payments = db.relationship('GroupPayment', backref='family', lazy='dynamic')
    
    # ========== METHODS ==========
    
    def generate_family_code(self):
        """
        Generate unique family code
        
        Format: FAM-YYYY-XXXX
        Example: FAM-2024-0001
        """
        from datetime import datetime
        current_year = datetime.now().year
        
        # Get the last family code for this year
        last_family = Family.query.filter(
            Family.family_code.like(f'FAM-{current_year}-%')
        ).order_by(Family.family_code.desc()).first()
        
        if last_family:
            # Extract number from last code and increment
            try:
                last_num = int(last_family.family_code.split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        # Format: FAM-YYYY-XXXX
        self.family_code = f'FAM-{current_year}-{new_num:04d}'
    
    def validate_cnic(self, cnic):
        """
        Validate Pakistani CNIC format
        
        Format: XXXXX-XXXXXXX-X
        Example: 12345-1234567-1
        """
        if not cnic:
            return True  # CNIC is optional
        
        pattern = r'^\d{5}-\d{7}-\d{1}$'
        return bool(re.match(pattern, cnic))
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<Family {self.family_code} - {self.father_name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'family_code': self.family_code,
            'father_name': self.father_name,
            'father_cnic': self.father_cnic,
            'father_contact': self.father_contact,
            'mother_name': self.mother_name,
            'address': self.address,
            'students_count': self.students.count()
        }
