"""
Student Model

This is the core model representing students in the school.

Why this model?
- Central to the entire system
- All fees are associated with students
- All payments are made for students
- Reports are student-based

This model has relationships with:
- ClassGrade (which class the student is in)
- Family (if student has siblings)
- FeePayment (all payments made by/for this student)
"""

from app import db
from datetime import datetime, date
from sqlalchemy import event


class Student(db.Model):
    """
    Student Model
    
    Represents a student in the school.
    This is the central entity - everything revolves around students.
    
    Table name: student
    """
    
    __tablename__ = 'student'
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Student ID (unique identifier, auto-generated: SCH-YYYY-XXXX)
    # Format: SCH-2024-0001
    # This is what appears on receipts and reports
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Name fields
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    
    # Date of birth
    date_of_birth = db.Column(db.Date, nullable=False)
    
    # Gender: M (Male), F (Female), O (Other)
    gender = db.Column(db.String(10), nullable=False)
    
    # Class/Grade (Foreign Key)
    # Many students belong to one class
    class_grade_id = db.Column(db.Integer, db.ForeignKey('class_grade.id'), nullable=True)
    
    # Admission details
    admission_date = db.Column(db.Date, nullable=False)
    admission_number = db.Column(db.String(50), unique=True, nullable=False, index=True)  # Auto-generated
    
    # Contact information (removed student's own contact)
    address = db.Column(db.Text, nullable=True)
    
    # Parent/Guardian information
    parent_guardian_name = db.Column(db.String(100), nullable=False)
    parent_primary_contact = db.Column(db.String(20), nullable=False)  # Primary contact
    parent_secondary_contact = db.Column(db.String(20), nullable=True)  # Secondary contact (optional)
    
    # Family (Foreign Key - for grouping siblings)
    # Many students can belong to one family
    # Nullable: Student might not have siblings in the school
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True, index=True)
    
    # Active status: Can deactivate without deleting
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ========== RELATIONSHIPS ==========
    # One student can have many fee payments
    fee_payments = db.relationship('FeePayment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    
    # ========== METHODS ==========
    
    def generate_student_id(self):
        """
        Generate unique student ID
        
        Format: SCH-YYYY-XXXX
        Example: SCH-2024-0001
        
        This is called automatically when a student is created.
        """
        from datetime import datetime
        current_year = datetime.now().year
        
        # Get the last student ID for this year
        last_student = Student.query.filter(
            Student.student_id.like(f'SCH-{current_year}-%')
        ).order_by(Student.student_id.desc()).first()
        
        if last_student:
            # Extract number from last ID and increment
            try:
                last_num = int(last_student.student_id.split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        # Format: SCH-YYYY-XXXX
        self.student_id = f'SCH-{current_year}-{new_num:04d}'
    
    def get_full_name(self):
        """Get student's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        """Calculate student's age"""
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<Student {self.student_id} - {self.get_full_name()}>'
    
    def to_dict(self):
        """Convert to dictionary (useful for JSON/Excel export)"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'father_name': self.father_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.get_age(),
            'gender': self.gender,
            'class_name': self.class_grade.class_name if self.class_grade else None,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'admission_number': self.admission_number,
            'address': self.address,
            'parent_guardian_name': self.parent_guardian_name,
            'parent_primary_contact': self.parent_primary_contact,
            'parent_secondary_contact': self.parent_secondary_contact,
            'is_active': self.is_active
        }


# ========== EVENT LISTENER ==========
# This automatically generates student_id and admission_number when a new student is created
@event.listens_for(Student, 'before_insert')
def generate_student_ids_before_insert(mapper, connection, target):
    """
    Event listener: Automatically generate student_id and admission_number before inserting
    
    This runs automatically when a new Student is created.
    No need to manually call generate_student_id() or generate_admission_number().
    """
    if not target.student_id:
        target.generate_student_id()
    if not target.admission_number:
        target.generate_admission_number()