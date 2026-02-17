# Database Schema Reference

## Entity Relationship Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Student   │────────▶│ FeePayment   │────────▶│ FeeStructure│
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │
      │                        │
      │                        ▼
      │                 ┌──────────────┐
      │                 │   Receipt    │
      │                 └──────────────┘
      │
      ▼
┌─────────────┐
│    Class    │
└─────────────┘
```

## Detailed Model Relationships

### 1. Student Model
**Table Name**: `student`

**Fields**:
- `id` (Primary Key, Auto)
- `student_id` (CharField, Unique, Max 50) - Format: SCH-YYYY-XXXX
- `first_name` (CharField, Max 100)
- `last_name` (CharField, Max 100)
- `father_name` (CharField, Max 100)
- `date_of_birth` (DateField)
- `gender` (CharField, Choices: M/F/O)
- `class_grade` (ForeignKey → Class)
- `admission_date` (DateField)
- `admission_number` (CharField, Max 50, Unique)
- `contact_number` (CharField, Max 20)
- `address` (TextField)
- `parent_guardian_name` (CharField, Max 100)
- `parent_contact` (CharField, Max 20)
- `is_active` (BooleanField, Default=True)
- `created_at` (DateTimeField, Auto)
- `updated_at` (DateTimeField, Auto)

**Relationships**:
- One-to-Many with FeePayment
- Many-to-One with Class

---

### 2. Class/Grade Model
**Table Name**: `class_grade`

**Fields**:
- `id` (Primary Key, Auto)
- `class_name` (CharField, Max 50) - e.g., "Class 1", "Grade 5"
- `class_code` (CharField, Max 10, Unique) - e.g., "C1", "G5"
- `order` (IntegerField) - For sorting
- `is_active` (BooleanField, Default=True)
- `created_at` (DateTimeField, Auto)

**Relationships**:
- One-to-Many with Student
- Many-to-Many with FeeStructure

---

### 3. Academic Year Model
**Table Name**: `academic_year`

**Fields**:
- `id` (Primary Key, Auto)
- `year_name` (String, Max 50) - e.g., "2024-2025"
- `start_date` (Date)
- `end_date` (Date)
- `is_current` (Boolean, Default=False)
- `created_at` (DateTime, Auto)

**Relationships**:
- One-to-Many with FeeStructure
- One-to-Many with FeePayment

**Why Academic Year Model is Required?**
The Academic Year model is essential for:
1. **Fee Structure Management**: Different academic years may have different fee amounts (e.g., fees increase each year)
2. **Historical Data**: Track which fees belong to which academic year for proper record-keeping
3. **Reporting**: Generate reports specific to an academic year (e.g., "Total fees collected in 2024-2025")
4. **Student Progression**: When students move to the next class, it's usually tied to a new academic year
5. **Fee Assignment**: When assigning fees, you need to know which academic year they belong to
6. **Defaulter Tracking**: Calculate defaulters based on the current academic year's fees

**Example Scenario**: 
- In 2024-2025, monthly fee for Class 5 is Rs. 5000
- In 2025-2026, monthly fee for Class 5 is Rs. 5500 (increased)
- Without Academic Year, you can't distinguish between these different fee structures

**Alternative**: If you only manage one academic year at a time and don't need historical tracking, you could simplify by storing the academic year as a string field in FeeStructure instead of a separate model. However, having a separate model is more flexible and recommended for proper data organization.

---

### 4. Fee Structure Model
**Table Name**: `fee_structure`

**Fields**:
- `id` (Primary Key, Auto)
- `fee_type` (CharField, Choices)
  - ADMISSION
  - MONTHLY
  - STATIONARY
  - EXAM
  - RENEWAL
  - OTHER
- `fee_name` (CharField, Max 100) - Custom name
- `amount` (DecimalField, Max 10 digits, 2 decimal places)
- `academic_year` (ForeignKey → AcademicYear)
- `applicable_classes` (ManyToManyField → Class)
- `due_date_offset` (IntegerField) - Days from assignment to due date
- `is_recurring` (BooleanField) - For monthly fees
- `is_active` (BooleanField, Default=True)
- `created_at` (DateTimeField, Auto)
- `updated_at` (DateTimeField, Auto)

**Relationships**:
- Many-to-Many with Class
- Many-to-One with AcademicYear
- One-to-Many with FeePayment

---

### 5. Fee Payment Model
**Table Name**: `fee_payment`

**Fields**:
- `id` (Primary Key, Auto)
- `student` (ForeignKey → Student, CASCADE)
- `fee_structure` (ForeignKey → FeeStructure, PROTECT)
- `amount` (DecimalField, Max 10 digits, 2 decimal places)
- `payment_method` (CharField, Choices)
  - CASH
  - EASYPAISA
  - JAZZCASH
  - BANK_TRANSFER
- `payment_date` (DateField)
- `due_date` (DateField)
- `status` (CharField, Choices)
  - PENDING
  - PAID
  - PARTIAL
  - OVERDUE
- `receipt_number` (CharField, Max 50, Unique, Nullable) - Format: RCP-YYYY-XXXXX
- `transaction_id` (CharField, Max 100, Nullable) - For digital payments
- `account_name` (CharField, Max 100, Nullable) - For digital payments
- `remarks` (TextField, Optional)
- `created_by` (ForeignKey → User)
- `created_at` (DateTimeField, Auto)
- `updated_at` (DateTimeField, Auto)

**Relationships**:
- Many-to-One with Student
- Many-to-One with FeeStructure
- One-to-One with PaymentReceipt

**Indexes**:
- Index on `student_id`
- Index on `status`
- Index on `payment_date`
- Index on `due_date`
- Unique constraint on `transaction_id` (when not null)

---

### 6. Payment Receipt Model
**Table Name**: `payment_receipt`

**Fields**:
- `id` (Primary Key, Auto)
- `payment` (OneToOneField → FeePayment, CASCADE)
- `receipt_number` (CharField, Max 50, Unique)
- `receipt_date` (DateField)
- `pdf_file_path` (CharField, Max 255, Nullable)
- `created_at` (DateTimeField, Auto)

**Relationships**:
- One-to-One with FeePayment

---

### 7. User/Admin Model
**Table Name**: `user`

**Fields**:
- `id` (Primary Key, Auto)
- `username` (String, Unique, Max 50)
- `email` (String, Max 100, Optional)
- `password_hash` (String, Max 255)
- `is_active` (Boolean, Default=True)
- `created_at` (DateTime, Auto)

**Additional Profile** (Optional):
**Table Name**: `admin_profile`

**Fields**:
- `id` (Primary Key, Auto)
- `user` (OneToOneField → User, CASCADE)
- `phone_number` (CharField, Max 20, Optional)
- `designation` (CharField, Max 100, Optional)
- `created_at` (DateTimeField, Auto)

---

## Database Constraints

### Unique Constraints
1. `Student.student_id` - Must be unique
2. `Student.admission_number` - Must be unique
3. `FeePayment.receipt_number` - Must be unique
4. `FeePayment.transaction_id` - Must be unique when not null
5. `Class.class_code` - Must be unique
6. `AcademicYear.year_name` - Should be unique (enforced in application)

### Foreign Key Constraints
- `FeePayment.student` → CASCADE on delete (if student deleted, payments deleted)
- `FeePayment.fee_structure` → PROTECT on delete (cannot delete fee structure if payments exist)
- `Student.class_grade` → SET_NULL on delete (if class deleted, set to null)

### Check Constraints
- `FeePayment.amount` > 0
- `FeeStructure.amount` > 0
- `AcademicYear.end_date` > `start_date`
- `FeePayment.payment_date` <= today (or allow future for advance payments)

---

## Indexes for Performance

### Student Table
- Index on `student_id`
- Index on `admission_number`
- Index on `class_grade_id`
- Index on `is_active`
- Composite index on `(class_grade_id, is_active)`

### FeePayment Table
- Index on `student_id`
- Index on `status`
- Index on `payment_date`
- Index on `due_date`
- Index on `fee_structure_id`
- Composite index on `(student_id, status)`
- Composite index on `(status, due_date)`

### FeeStructure Table
- Index on `fee_type`
- Index on `academic_year_id`
- Index on `is_active`

---

## Sample Data Structure

### Student Example
```json
{
  "student_id": "SCH-2024-0001",
  "first_name": "Ahmed",
  "last_name": "Khan",
  "father_name": "Muhammad Khan",
  "date_of_birth": "2010-05-15",
  "gender": "M",
  "class_grade": 5,  // Class ID
  "section": "A",
  "admission_date": "2024-01-15",
  "admission_number": "ADM-2024-001",
  "contact_number": "+92-300-1234567",
  "address": "123 Main Street, City",
  "parent_guardian_name": "Muhammad Khan",
  "parent_contact": "+92-300-1234567",
  "is_active": true
}
```

### FeePayment Example (Cash)
```json
{
  "student": 1,
  "fee_structure": 2,  // Monthly Fee
  "amount": 5000.00,
  "payment_method": "CASH",
  "payment_date": "2024-03-15",
  "due_date": "2024-03-01",
  "status": "PAID",
  "receipt_number": "RCP-2024-00001",
  "transaction_id": null,
  "account_name": null
}
```

### FeePayment Example (Easypaisa)
```json
{
  "student": 1,
  "fee_structure": 2,
  "amount": 5000.00,
  "payment_method": "EASYPAISA",
  "payment_date": "2024-03-14",
  "due_date": "2024-03-01",
  "status": "PAID",
  "receipt_number": "RCP-2024-00002",
  "transaction_id": "EP123456789",
  "account_name": "Ahmed Khan"
}
```

---

## Query Optimization Notes

1. **Defaulter Calculation**: Use database aggregation for better performance
2. **Payment History**: Use SQLAlchemy joinedload/eager loading for student and fee_structure
3. **Reports**: Consider database views for complex aggregations
4. **Search**: Use LIKE queries or full-text search for student names

---

## Excel Export Requirements

### Export Students to Excel
**Fields to Include**:
- Student ID
- First Name
- Last Name
- Father Name
- Date of Birth
- Gender
- Class/Grade
- Admission Date
- Admission Number
- Contact Number
- Address
- Parent/Guardian Name
- Parent Contact
- Status (Active/Inactive)

**Formatting**:
- Header row with bold, colored background
- Auto-adjust column widths
- Date formatting (YYYY-MM-DD)
- Freeze header row

### Export Defaulters to Excel
**Fields to Include**:
- Student ID
- Student Name (Full)
- Class/Grade
- Defaulter Status (RED/BLUE/GREY) - with color coding
- Total Pending Amount
- Months Overdue
- Oldest Unpaid Fee Date
- Number of Unpaid Fees
- Contact Number
- Parent/Guardian Name
- Parent Contact
- List of Unpaid Fees (can be in separate sheet or comma-separated)

**Formatting**:
- Color code status column (RED=red, BLUE=blue, GREY=gray)
- Header row with bold, colored background
- Auto-adjust column widths
- Currency formatting for amounts
- Date formatting

### Export Payment History to Excel
**Fields to Include**:
- Receipt Number
- Payment Date
- Student ID
- Student Name
- Fee Type
- Amount
- Payment Method
- Transaction ID (if applicable)
- Account Name (if applicable)
- Status
- Due Date

**Formatting**:
- Header row with bold, colored background
- Auto-adjust column widths
- Currency formatting for amounts
- Date formatting
- Filterable columns

---

## Migration Strategy (Flask-Migrate)

1. Create base models using SQLAlchemy
2. Initialize Flask-Migrate: `flask db init`
3. Create initial migration: `flask db migrate -m "Initial migration"`
4. Apply migration: `flask db upgrade`
5. Add indexes after initial data load
6. Add constraints after data validation
7. Consider data migration scripts for existing data

