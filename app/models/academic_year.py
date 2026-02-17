"""
Academic Year Model

This represents an academic year (e.g., 2024-2025, 2025-2026)

Why this model?
- Fees change from year to year
- Need to track which fees belong to which year
- Reports are often year-specific
- Students progress through years

Example: 
- 2024-2025: Monthly fee = Rs. 5000
- 2025-2026: Monthly fee = Rs. 5500 (increased)
Without Academic Year, we can't distinguish between these!
"""

from app import db
from datetime import datetime, date


class AcademicYear(db.Model):
    """
    Academic Year Model
    
    Represents an academic year period.
    Each fee structure belongs to an academic year.
    This allows fees to change from year to year.
    
    Table name: academic_year
    """
    
    __tablename__ = 'academic_year'
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Year name (e.g., "2024-2025", "2025-2026")
    year_name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    
    # Start date of academic year
    start_date = db.Column(db.Date, nullable=False)
    
    # End date of academic year
    end_date = db.Column(db.Date, nullable=False)
    
    # Is this the current academic year?
    # Only one academic year should be marked as current
    is_current = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ========== RELATIONSHIPS ==========
    # One academic year can have many fee structures
    fee_structures = db.relationship('FeeStructure', backref='academic_year', lazy='dynamic')
    
    # ========== METHODS ==========
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<AcademicYear {self.year_name}>'
    
    @staticmethod
    def get_current():
        """Get the current academic year"""
        return AcademicYear.query.filter_by(is_current=True).first()
    
    @staticmethod
    def set_current(year_id):
        """
        Set an academic year as current
        
        This automatically unsets any other current year.
        Only one year can be current at a time.
        """
        # Unset all current years
        AcademicYear.query.update({'is_current': False})
        
        # Set the specified year as current
        year = AcademicYear.query.get(year_id)
        if year:
            year.is_current = True
            db.session.commit()
            return True
        return False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'year_name': self.year_name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current
        }
