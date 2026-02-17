"""
Class/Grade Model

This represents the class/grade levels in the school (e.g., Class 1, Class 2, Grade 5, etc.)

Why this model?
- Students belong to a class
- Fee structures are assigned to specific classes
- Reports are often class-wise
- Classes have a hierarchy (order)

Example: Class 1, Class 2, Class 3... or Grade 1, Grade 2...
"""

from app import db
from datetime import datetime


class ClassGrade(db.Model):
    """
    Class/Grade Model
    
    Represents a class or grade level in the school.
    Each student belongs to one class.
    Fee structures can be assigned to multiple classes.
    
    Table name: class_grade
    """
    
    __tablename__ = 'class_grade'
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Class name (e.g., "Class 1", "Grade 5", "Nursery")
    class_name = db.Column(db.String(50), nullable=False)
    
    # Class code (short identifier, e.g., "C1", "G5", "NUR")
    # Unique: No two classes can have the same code
    class_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    
    # Order: For sorting classes (1 = first class, 2 = second, etc.)
    # Helps display classes in correct order (Class 1 before Class 2)
    order = db.Column(db.Integer, nullable=False, default=0)
    
    # Active status: Can deactivate a class without deleting it
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ========== RELATIONSHIPS ==========
    # One class can have many students
    # This creates a "students" attribute on ClassGrade
    # Example: class1.students returns all students in Class 1
    students = db.relationship('Student', backref='class_grade', lazy='dynamic')
    
    # Many-to-Many relationship with FeeStructure
    # One class can have many fee structures
    # One fee structure can apply to many classes
    # This creates an "applicable_classes" attribute on FeeStructure
    fee_structures = db.relationship(
        'FeeStructure',
        secondary='fee_structure_classes',  # Junction table name
        back_populates='applicable_classes',
        lazy='dynamic'
    )
    
    # ========== METHODS ==========
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<ClassGrade {self.class_name}>'
    
    def to_dict(self):
        """Convert to dictionary (useful for JSON APIs)"""
        return {
            'id': self.id,
            'class_name': self.class_name,
            'class_code': self.class_code,
            'order': self.order,
            'is_active': self.is_active
        }
