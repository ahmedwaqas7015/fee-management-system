# Phase 2 Teaching Guide - Database Models & Migrations

## 🎓 What We Just Built

Congratulations! We've completed **Phase 2: Database Models & Migrations**. This is the foundation of our entire system - all the data structures that will store information.

---

## 📊 Database Models Created

We created **9 database models** (tables):

### 1. **User Model** ✅ (Already existed)
- Stores admin user information
- Handles authentication

### 2. **ClassGrade Model** ✅
- Represents classes/grades (Class 1, Class 2, etc.)
- Has order for sorting
- Links to students and fee structures

### 3. **AcademicYear Model** ✅
- Represents academic years (2024-2025, etc.)
- Tracks which year is current
- Links to fee structures

### 4. **Family Model** ✅
- Groups siblings together
- Enables family/group payments
- Stores father's information

### 5. **Student Model** ✅
- Core model - represents students
- Auto-generates student ID (SCH-YYYY-XXXX)
- Links to class, family, and payments

### 6. **FeeStructure Model** ✅
- Defines fee types and amounts
- Links to classes (many-to-many)
- Links to academic year

### 7. **FeePayment Model** ✅
- Tracks individual payments
- Auto-generates receipt numbers
- Links to student, fee structure, and group payment

### 8. **GroupPayment Model** ✅
- Tracks family/group payments
- Links multiple students together
- Single receipt for all siblings

### 9. **PaymentReceipt Model** ✅
- Stores receipt information
- Can be for individual or group payments
- Stores PDF file path

---

## 🔗 Database Relationships Explained

### One-to-Many Relationships

**What is it?**
- One record in Table A can have many records in Table B
- Example: One Class can have many Students

**In our system:**
```python
# ClassGrade → Student (One-to-Many)
class ClassGrade:
    students = db.relationship('Student', backref='class_grade')

# One class has many students
class1.students  # Returns all students in Class 1
student.class_grade  # Returns the class the student belongs to
```

**Examples:**
- One Class → Many Students
- One Family → Many Students (siblings)
- One Academic Year → Many Fee Structures
- One Student → Many Fee Payments
- One Family → Many Group Payments

### Many-to-Many Relationships

**What is it?**
- Records in Table A can relate to many records in Table B
- And vice versa
- Requires a junction table

**In our system:**
```python
# FeeStructure ↔ ClassGrade (Many-to-Many)
# One fee structure can apply to many classes
# One class can have many fee structures

fee_structure_classes = db.Table(
    'fee_structure_classes',
    db.Column('fee_structure_id', ...),
    db.Column('class_grade_id', ...)
)

class FeeStructure:
    applicable_classes = db.relationship(
        'ClassGrade',
        secondary=fee_structure_classes,
        back_populates='fee_structures'
    )
```

**Example:**
- Monthly Fee (Rs. 5000) applies to Class 1, Class 2, Class 3
- Class 5 has Monthly Fee, Exam Fee, Stationary Fee

### One-to-One Relationships

**What is it?**
- One record in Table A relates to exactly one record in Table B
- Example: One Payment → One Receipt

**In our system:**
```python
# FeePayment → PaymentReceipt (One-to-One)
class FeePayment:
    receipt = db.relationship('PaymentReceipt', uselist=False)

# One payment has one receipt
payment.receipt  # Returns the receipt for this payment
```

---

## 🔑 Key Concepts Explained

### 1. **Primary Keys**

**What is it?**
- Unique identifier for each row
- Every table has one
- Usually auto-incrementing integer

**Example:**
```python
id = db.Column(db.Integer, primary_key=True)
# First student: id = 1
# Second student: id = 2
```

**Why important?**
- Uniquely identifies each record
- Used in foreign keys to link tables

### 2. **Foreign Keys**

**What is it?**
- Links one table to another
- References the primary key of another table
- Creates relationships

**Example:**
```python
# Student table has a foreign key to ClassGrade
class_grade_id = db.Column(
    db.Integer, 
    db.ForeignKey('class_grade.id')
)
```

**What it means:**
- Each student belongs to one class
- The `class_grade_id` points to which class

### 3. **Indexes**

**What is it?**
- Makes database queries faster
- Like an index in a book - helps find data quickly

**Example:**
```python
student_id = db.Column(..., index=True)
# Searching by student_id is now fast!
```

**When to use:**
- Fields you search frequently
- Foreign keys (usually auto-indexed)
- Unique fields

### 4. **Auto-Generated Fields**

**What is it?**
- Fields that are automatically created
- No manual input needed

**In our system:**
```python
# Student ID: SCH-2024-0001
# Receipt Number: RCP-2024-00001
# Family Code: FAM-2024-0001
```

**How it works:**
- Event listeners automatically generate values
- Format: PREFIX-YYYY-XXXX
- Increments automatically

### 5. **Cascade Operations**

**What is it?**
- What happens when parent record is deleted
- Options: CASCADE, RESTRICT, SET NULL

**Examples:**
```python
# CASCADE: Delete student, delete all their payments
student_id = db.ForeignKey(..., ondelete='CASCADE')

# RESTRICT: Can't delete fee structure if payments exist
fee_structure_id = db.ForeignKey(..., ondelete='RESTRICT')

# SET NULL: Delete group payment, set group_payment_id to NULL
group_payment_id = db.ForeignKey(..., ondelete='SET NULL')
```

---

## 🗄️ Database Migrations (Flask-Migrate)

### What are Migrations?

**Migrations** are scripts that:
- Create database tables
- Modify table structure
- Add/remove columns
- Track database changes over time

**Why use migrations?**
- Version control for database
- Can rollback changes
- Team collaboration
- Production deployments

### How Migrations Work

**1. Create Migration:**
```bash
flask db migrate -m "Description"
```
- Analyzes your models
- Generates SQL to create/modify tables
- Creates a migration file

**2. Apply Migration:**
```bash
flask db upgrade
```
- Runs the migration
- Creates/modifies tables in database

**3. Rollback Migration:**
```bash
flask db downgrade
```
- Undoes the last migration
- Useful if something goes wrong

### Migration Files

**Location:** `migrations/versions/`

**Example:** `8960f76fde21_initial_migration_all_models.py`

**Contains:**
- `upgrade()`: What to do when applying migration
- `downgrade()`: What to do when rolling back

---

## 📝 Model Methods Explained

### Instance Methods

**Methods that work on a single record:**

```python
# Student model
student.get_full_name()  # Returns "Ahmed Khan"
student.get_age()        # Returns 14
student.to_dict()        # Returns dictionary representation
```

### Class Methods (Static Methods)

**Methods that work on the entire table:**

```python
# AcademicYear model
AcademicYear.get_current()  # Returns current academic year
AcademicYear.set_current(year_id)  # Sets current year
```

### Event Listeners

**Automatically run when something happens:**

```python
@event.listens_for(Student, 'before_insert')
def generate_student_id_before_insert(...):
    # Automatically runs when creating a new student
    # Generates student_id before saving
```

**Events:**
- `before_insert`: Before creating new record
- `before_update`: Before updating record
- `after_insert`: After creating new record

---

## 🔍 Querying the Database

### Basic Queries

```python
# Get all students
students = Student.query.all()

# Get one student by ID
student = Student.query.get(1)

# Get student by student_id
student = Student.query.filter_by(student_id='SCH-2024-0001').first()

# Get active students only
active_students = Student.query.filter_by(is_active=True).all()
```

### Filtering

```python
# Students in Class 5
class5_students = Student.query.filter_by(class_grade_id=5).all()

# Students with pending payments
pending = FeePayment.query.filter_by(status='PENDING').all()

# Students in a family
family_students = Student.query.filter_by(family_id=1).all()
```

### Relationships

```python
# Get all students in a class
class1 = ClassGrade.query.filter_by(class_code='C1').first()
students = class1.students.all()

# Get student's payments
student = Student.query.get(1)
payments = student.fee_payments.all()

# Get family's students
family = Family.query.get(1)
siblings = family.students.all()
```

---

## 🎯 Real-World Examples

### Example 1: Creating a Student

```python
# Create a new student
student = Student(
    first_name="Ahmed",
    last_name="Khan",
    father_name="Muhammad Khan",
    date_of_birth=date(2010, 5, 15),
    gender="M",
    class_grade_id=5,  # Class 5
    admission_date=date(2024, 4, 1),
    admission_number="ADM-2024-0001",
    parent_guardian_name="Muhammad Khan",
    parent_contact="+92-300-1234567"
)
# student_id is auto-generated: SCH-2024-0001

db.session.add(student)
db.session.commit()
```

### Example 2: Creating a Family Payment

```python
# 1. Get family
family = Family.query.filter_by(family_code='FAM-2024-0001').first()

# 2. Get students in family
students = family.students.all()  # [Ahmed, Ali, Fatima]

# 3. Create group payment
group_payment = GroupPayment(
    family_id=family.id,
    total_amount=12500.00,  # Sum of all fees
    payment_method='CASH',
    payment_date=date.today(),
    students_count=3,
    created_by_id=admin.id
)
# Receipt number auto-generated: RCP-2024-00001

# 4. Create individual payments linked to group payment
for student in students:
    payment = FeePayment(
        student_id=student.id,
        fee_structure_id=monthly_fee.id,
        amount=5000.00,
        payment_method='CASH',
        payment_date=date.today(),
        due_date=date.today() + timedelta(days=30),
        group_payment_id=group_payment.id,
        created_by_id=admin.id
    )
    db.session.add(payment)

db.session.add(group_payment)
db.session.commit()
```

### Example 3: Finding Defaulters

```python
# Find students with overdue payments
from datetime import date

overdue_payments = FeePayment.query.filter(
    FeePayment.status.in_(['PENDING', 'OVERDUE']),
    FeePayment.due_date < date.today()
).all()

# Group by student
defaulters = {}
for payment in overdue_payments:
    student = payment.student
    if student.id not in defaulters:
        defaulters[student.id] = {
            'student': student,
            'payments': [],
            'total': 0
        }
    defaulters[student.id]['payments'].append(payment)
    defaulters[student.id]['total'] += float(payment.amount)
```

---

## 🛠️ SQLAlchemy ORM Explained

### What is ORM?

**ORM = Object-Relational Mapping**

**What it does:**
- Maps Python classes to database tables
- Maps Python objects to database rows
- Lets you use Python instead of SQL

**Example:**
```python
# Instead of SQL:
# SELECT * FROM student WHERE id = 1;

# You write Python:
student = Student.query.get(1)
```

### Benefits

1. **Type Safety**: Python knows the data types
2. **No SQL Injection**: ORM handles escaping
3. **Database Agnostic**: Works with SQLite, PostgreSQL, MySQL
4. **Easy Relationships**: Navigate relationships easily

---

## 📚 Important Patterns

### 1. **Lazy Loading vs Eager Loading**

**Lazy Loading (default):**
```python
students = class1.students  # Doesn't query yet
for student in students:   # Queries when iterating
    print(student.name)
```

**Eager Loading (faster for many relationships):**
```python
from sqlalchemy.orm import joinedload

students = Student.query.options(
    joinedload(Student.class_grade)
).all()
# Loads class information immediately
```

### 2. **Session Management**

**Always use app context:**
```python
with app.app_context():
    # Database operations here
    student = Student.query.get(1)
```

**Why?**
- Flask needs to know which app you're using
- Provides database connection
- Manages transactions

### 3. **Transactions**

**What is a transaction?**
- Group of operations that succeed or fail together
- If one fails, all are rolled back

**Example:**
```python
try:
    # Create student
    student = Student(...)
    db.session.add(student)
    
    # Create payment
    payment = FeePayment(...)
    db.session.add(payment)
    
    # If both succeed, commit
    db.session.commit()
except:
    # If anything fails, rollback
    db.session.rollback()
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Table doesn't exist"
**Solution:** Run migrations: `flask db upgrade`

### Issue 2: "Circular import"
**Solution:** Import models in correct order in `__init__.py`

### Issue 3: "Foreign key constraint fails"
**Solution:** Make sure referenced record exists first

### Issue 4: "SQLite doesn't support PROTECT"
**Solution:** Use RESTRICT instead (SQLite compatible)

---

## ✅ Phase 2 Checklist

- [x] ClassGrade model created
- [x] AcademicYear model created
- [x] Family model created
- [x] Student model created
- [x] FeeStructure model created
- [x] FeePayment model created
- [x] GroupPayment model created
- [x] PaymentReceipt model created
- [x] All models imported in `__init__.py`
- [x] Flask-Migrate configured
- [x] Initial migration created
- [x] Migration applied
- [x] Sample data script created
- [x] Sample data generated

---

## 🎓 What You Learned

1. ✅ **Database Models**: How to create SQLAlchemy models
2. ✅ **Relationships**: One-to-Many, Many-to-Many, One-to-One
3. ✅ **Foreign Keys**: How to link tables together
4. ✅ **Auto-Generation**: Event listeners for automatic values
5. ✅ **Migrations**: Version control for database
6. ✅ **Querying**: How to retrieve data from database
7. ✅ **Transactions**: How to ensure data consistency

---

## 🚀 Next Steps (Phase 3)

In Phase 3, we'll build:
- Student Management UI
- Add/Edit/View students
- Search and filter
- Family management
- Excel export

**You'll learn:**
- Flask routes and views
- Form handling with WTForms
- Template rendering
- User input validation

---

## 💡 Pro Tips

1. **Always use migrations** - Don't modify database directly
2. **Test relationships** - Make sure foreign keys work
3. **Use indexes** - On fields you search frequently
4. **Validate data** - At model level and form level
5. **Use transactions** - For operations that must succeed together

---

**Great job completing Phase 2! You now have a complete database structure!** 🎉
