"""
Fee Structure Model

This defines the types of fees and their amounts.

Why this model?
- Defines what fees exist (Monthly, Admission, Exam, etc.)
- Sets the amount for each fee type
- Links fees to specific classes
- Links fees to academic years (fees can change year to year)

Example:
- Monthly Fee for Class 5 in 2024-2025: Rs. 5,000
- Monthly Fee for Class 5 in 2025-2026: Rs. 5,500 (increased)
- Exam Fee for Class 5 in 2024-2025: Rs. 2,000
"""

from app import db
from datetime import datetime

# Junction table for Many-to-Many relationship
# This is needed because one fee structure can apply to many classes
# and one class can have many fee structures
fee_structure_classes = db.Table(
    'fee_structure_classes',
    db.Column('fee_structure_id', db.Integer, db.ForeignKey('fee_structure.id'), primary_key=True),
    db.Column('class_grade_id', db.Integer, db.ForeignKey('class_grade.id'), primary_key=True)
)


class FeeStructure(db.Model):
    """
    Fee Structure Model
    
    Defines fee types and their amounts.
    Can be assigned to multiple classes.
    Belongs to an academic year.
    
    Table name: fee_structure
    """
    
    __tablename__ = 'fee_structure'
    
    # ========== FEE TYPES ==========
    # These are the choices for fee_type
    FEE_TYPE_ADMISSION = 'ADMISSION'
    FEE_TYPE_MONTHLY = 'MONTHLY'
    FEE_TYPE_STATIONARY = 'STATIONARY/BOOKS'
    FEE_TYPE_EXAM = 'EXAM'
    FEE_TYPE_RENEWAL = 'ADMISSION RENEWAL'
    FEE_TYPE_OTHER = 'OTHER'
    
    FEE_TYPES = [
        (FEE_TYPE_ADMISSION, 'Admission Fee'),
        (FEE_TYPE_MONTHLY, 'Monthly Fee'),
        (FEE_TYPE_STATIONARY, 'Stationary/Books Fee'),
        (FEE_TYPE_EXAM, 'Exam Fee'),
        (FEE_TYPE_RENEWAL, 'Admission Renewal Fee'),
        (FEE_TYPE_OTHER, 'Other Fee')
    ]
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Fee type (from choices above)
    fee_type = db.Column(db.String(50), nullable=False, index=True)
    
    # Custom fee name (e.g., "Monthly Fee - March", "Final Exam Fee")
    fee_name = db.Column(db.String(100), nullable=False)
    
    # Amount (decimal with 2 decimal places)
    # Example: 5000.00
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Academic Year (Foreign Key)
    # Fees belong to a specific academic year
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_year.id'), nullable=False, index=True)
    
    # Due date offset: Days from assignment to due date
    # Example: 30 means fee is due 30 days after assignment
    due_date_offset = db.Column(db.Integer, default=30, nullable=False)
    
    # Is this a recurring fee? (e.g., monthly fees)
    is_recurring = db.Column(db.Boolean, default=False, nullable=False)
    
    # Active status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ========== RELATIONSHIPS ==========
    # Many-to-Many with ClassGrade
    # One fee structure can apply to many classes
    # One class can have many fee structures
    applicable_classes = db.relationship(
        'ClassGrade',
        secondary=fee_structure_classes,
        back_populates='fee_structures',
        lazy='dynamic'
    )
    
    # One fee structure can have many fee payments
    fee_payments = db.relationship('FeePayment', backref='fee_structure', lazy='dynamic')
    
    # ========== METHODS ==========
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<FeeStructure {self.fee_name} - Rs. {self.amount}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'fee_type': self.fee_type,
            'fee_name': self.fee_name,
            'amount': float(self.amount),
            'academic_year': self.academic_year.year_name if self.academic_year else None,
            'due_date_offset': self.due_date_offset,
            'is_recurring': self.is_recurring,
            'is_active': self.is_active,
            'applicable_classes': [c.class_name for c in self.applicable_classes.all()]
        }
