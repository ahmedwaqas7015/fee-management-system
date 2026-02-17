"""
Sample Data Generation Script

This script creates sample data for testing the system.
Run it after initializing the database.

Usage: python create_sample_data.py

This creates:
- Academic years
- Classes
- Families
- Students
- Fee structures
- Sample payments (optional)
"""

from app import create_app, db
from app.models import (
    User, ClassGrade, AcademicYear, Family, Student,
    FeeStructure, FeePayment
)
from datetime import date, datetime, timedelta

app = create_app('development')

def create_sample_data():
    """Create sample data for testing"""
    
    with app.app_context():
        print("=" * 60)
        print("Creating Sample Data for Fee Management System")
        print("=" * 60)
        
        # ========== 1. ACADEMIC YEARS ==========
        print("\n1. Creating Academic Years...")
        
        # Current academic year
        current_year = AcademicYear.query.filter_by(is_current=True).first()
        if not current_year:
            current_year = AcademicYear(
                year_name="2024-2025",
                start_date=date(2024, 4, 1),
                end_date=date(2025, 3, 31),
                is_current=True
            )
            db.session.add(current_year)
            print("   ✅ Created: 2024-2025 (Current)")
        else:
            print(f"   ✅ Already exists: {current_year.year_name} (Current)")
        
        # Previous year
        prev_year = AcademicYear.query.filter_by(year_name="2023-2024").first()
        if not prev_year:
            prev_year = AcademicYear(
                year_name="2023-2024",
                start_date=date(2023, 4, 1),
                end_date=date(2024, 3, 31),
                is_current=False
            )
            db.session.add(prev_year)
            print("   ✅ Created: 2023-2024")
        
        db.session.commit()
        
        # ========== 2. CLASSES ==========
        print("\n2. Creating Classes...")
        
        classes_data = [
            ("Nursery", "NUR", 1),
            ("Class 1", "C1", 2),
            ("Class 2", "C2", 3),
            ("Class 3", "C3", 4),
            ("Class 4", "C4", 5),
            ("Class 5", "C5", 6),
            ("Class 6", "C6", 7),
            ("Class 7", "C7", 8),
            ("Class 8", "C8", 9),
            ("Class 9", "C9", 10),
            ("Class 10", "C10", 11),
        ]
        
        created_classes = []
        for class_name, class_code, order in classes_data:
            existing = ClassGrade.query.filter_by(class_code=class_code).first()
            if not existing:
                class_grade = ClassGrade(
                    class_name=class_name,
                    class_code=class_code,
                    order=order,
                    is_active=True
                )
                db.session.add(class_grade)
                created_classes.append(class_grade)
                print(f"   ✅ Created: {class_name} ({class_code})")
            else:
                created_classes.append(existing)
                print(f"   ✅ Already exists: {class_name}")
        
        db.session.commit()
        
        # ========== 3. FAMILIES ==========
        print("\n3. Creating Sample Families...")
        
        families_data = [
            {
                "father_name": "Muhammad Ahmed Khan",
                "father_cnic": "12345-1234567-1",
                "father_contact": "+92-300-1234567",
                "mother_name": "Fatima Khan",
                "address": "123 Main Street, Karachi"
            },
            {
                "father_name": "Ali Hassan",
                "father_cnic": "23456-2345678-2",
                "father_contact": "+92-300-2345678",
                "address": "456 Park Avenue, Lahore"
            },
        ]
        
        created_families = []
        for family_data in families_data:
            existing = Family.query.filter_by(father_cnic=family_data["father_cnic"]).first()
            if not existing:
                family = Family(**family_data)
                family.generate_family_code()
                db.session.add(family)
                created_families.append(family)
                print(f"   ✅ Created: {family.family_code} - {family.father_name}")
            else:
                created_families.append(existing)
                print(f"   ✅ Already exists: {existing.family_code}")
        
        db.session.commit()
        
        # ========== 4. STUDENTS ==========
        print("\n4. Creating Sample Students...")
        
        # Get admin user for created_by
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("   ⚠️  Admin user not found! Run init_db.py first.")
            return
        
        students_data = [
            # Family 1 - 3 siblings
            {
                "first_name": "Ahmed",
                "last_name": "Khan",
                "father_name": "Muhammad Ahmed Khan",
                "date_of_birth": date(2010, 5, 15),
                "gender": "M",
                "class_grade": created_classes[5],  # Class 5
                "admission_date": date(2024, 4, 1),
                "admission_number": "ADM-2024-0001",
                "contact_number": "+92-300-1234567",
                "address": "123 Main Street, Karachi",
                "parent_guardian_name": "Muhammad Ahmed Khan",
                "parent_contact": "+92-300-1234567",
                "family": created_families[0] if created_families else None
            },
            {
                "first_name": "Ali",
                "last_name": "Khan",
                "father_name": "Muhammad Ahmed Khan",
                "date_of_birth": date(2012, 8, 20),
                "gender": "M",
                "class_grade": created_classes[3],  # Class 3
                "admission_date": date(2024, 4, 1),
                "admission_number": "ADM-2024-0002",
                "contact_number": "+92-300-1234567",
                "address": "123 Main Street, Karachi",
                "parent_guardian_name": "Muhammad Ahmed Khan",
                "parent_contact": "+92-300-1234567",
                "family": created_families[0] if created_families else None
            },
            {
                "first_name": "Fatima",
                "last_name": "Khan",
                "father_name": "Muhammad Ahmed Khan",
                "date_of_birth": date(2014, 3, 10),
                "gender": "F",
                "class_grade": created_classes[1],  # Class 1
                "admission_date": date(2024, 4, 1),
                "admission_number": "ADM-2024-0003",
                "contact_number": "+92-300-1234567",
                "address": "123 Main Street, Karachi",
                "parent_guardian_name": "Muhammad Ahmed Khan",
                "parent_contact": "+92-300-1234567",
                "family": created_families[0] if created_families else None
            },
            # Family 2 - 1 student
            {
                "first_name": "Hassan",
                "last_name": "Ali",
                "father_name": "Ali Hassan",
                "date_of_birth": date(2011, 7, 5),
                "gender": "M",
                "class_grade": created_classes[4],  # Class 4
                "admission_date": date(2024, 4, 1),
                "admission_number": "ADM-2024-0004",
                "contact_number": "+92-300-2345678",
                "address": "456 Park Avenue, Lahore",
                "parent_guardian_name": "Ali Hassan",
                "parent_contact": "+92-300-2345678",
                "family": created_families[1] if len(created_families) > 1 else None
            },
            # Individual student (no family)
            {
                "first_name": "Sara",
                "last_name": "Ahmed",
                "father_name": "Ahmed Ali",
                "date_of_birth": date(2009, 12, 25),
                "gender": "F",
                "class_grade": created_classes[6],  # Class 6
                "admission_date": date(2024, 4, 1),
                "admission_number": "ADM-2024-0005",
                "contact_number": "+92-300-3456789",
                "address": "789 Garden Road, Islamabad",
                "parent_guardian_name": "Ahmed Ali",
                "parent_contact": "+92-300-3456789",
                "family": None
            },
        ]
        
        created_students = []
        for student_data in students_data:
            existing = Student.query.filter_by(admission_number=student_data["admission_number"]).first()
            if not existing:
                student = Student(**student_data)
                # Student ID will be auto-generated by event listener
                db.session.add(student)
                created_students.append(student)
                db.session.flush()  # Flush to get the generated student_id
                print(f"   ✅ Created: {student.student_id} - {student.get_full_name()} ({student.class_grade.class_name if student.class_grade else 'No Class'})")
            else:
                created_students.append(existing)
                print(f"   ✅ Already exists: {existing.student_id}")
        
        db.session.commit()
        
        # ========== 5. FEE STRUCTURES ==========
        print("\n5. Creating Fee Structures...")
        
        fee_structures_data = [
            {
                "fee_type": FeeStructure.FEE_TYPE_ADMISSION,
                "fee_name": "Admission Fee",
                "amount": 10000.00,
                "academic_year": current_year,
                "due_date_offset": 7,
                "is_recurring": False,
                "applicable_classes": created_classes  # All classes
            },
            {
                "fee_type": FeeStructure.FEE_TYPE_MONTHLY,
                "fee_name": "Monthly Fee",
                "amount": 5000.00,
                "academic_year": current_year,
                "due_date_offset": 30,
                "is_recurring": True,
                "applicable_classes": created_classes[1:]  # Class 1 onwards
            },
            {
                "fee_type": FeeStructure.FEE_TYPE_EXAM,
                "fee_name": "Annual Exam Fee",
                "amount": 2000.00,
                "academic_year": current_year,
                "due_date_offset": 60,
                "is_recurring": False,
                "applicable_classes": created_classes[1:]  # Class 1 onwards
            },
            {
                "fee_type": FeeStructure.FEE_TYPE_STATIONARY,
                "fee_name": "Stationary/Books Fee",
                "amount": 3000.00,
                "academic_year": current_year,
                "due_date_offset": 15,
                "is_recurring": False,
                "applicable_classes": created_classes  # All classes
            },
        ]
        
        created_fee_structures = []
        for fee_data in fee_structures_data:
            applicable_classes = fee_data.pop("applicable_classes")
            existing = FeeStructure.query.filter_by(
                fee_type=fee_data["fee_type"],
                fee_name=fee_data["fee_name"],
                academic_year_id=current_year.id
            ).first()
            
            if not existing:
                fee_structure = FeeStructure(**fee_data)
                fee_structure.applicable_classes = applicable_classes
                db.session.add(fee_structure)
                created_fee_structures.append(fee_structure)
                print(f"   ✅ Created: {fee_structure.fee_name} - Rs. {fee_structure.amount}")
            else:
                created_fee_structures.append(existing)
                print(f"   ✅ Already exists: {existing.fee_name}")
        
        db.session.commit()
        
        print("\n" + "=" * 60)
        print("Sample Data Creation Complete!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  - Academic Years: {AcademicYear.query.count()}")
        print(f"  - Classes: {ClassGrade.query.count()}")
        print(f"  - Families: {Family.query.count()}")
        print(f"  - Students: {Student.query.count()}")
        print(f"  - Fee Structures: {FeeStructure.query.count()}")
        print("\n✅ You can now test the system with this sample data!")
        print("=" * 60)

if __name__ == '__main__':
    create_sample_data()
