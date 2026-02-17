"""
Fee Payment Model

This tracks individual fee payments made by students.

Why this model?
- Records every payment transaction
- Links payment to student and fee structure
- Tracks payment method (Cash, Easypaisa, etc.)
- Stores transaction details for digital payments
- Can be part of a group payment (family payment)

This is the core payment tracking model.
"""

from app import db
from datetime import datetime, date
from sqlalchemy import event


class FeePayment(db.Model):
    """
    Fee Payment Model
    
    Represents a single fee payment transaction.
    Can be an individual payment or part of a group payment (family).
    
    Table name: fee_payment
    """
    
    __tablename__ = 'fee_payment'
    
    # ========== PAYMENT METHODS ==========
    PAYMENT_CASH = 'CASH'
    PAYMENT_EASYPAISA = 'EASYPAISA'
    PAYMENT_JAZZCASH = 'JAZZCASH'
    PAYMENT_BANK_TRANSFER = 'BANK_TRANSFER'
    
    PAYMENT_METHODS = [
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_EASYPAISA, 'Easypaisa'),
        (PAYMENT_JAZZCASH, 'Jazzcash'),
        (PAYMENT_BANK_TRANSFER, 'Bank Transfer')
    ]
    
    # ========== PAYMENT STATUS ==========
    STATUS_PENDING = 'PENDING'
    STATUS_PAID = 'PAID'
    STATUS_PARTIAL = 'PARTIAL'
    STATUS_OVERDUE = 'OVERDUE'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_PARTIAL, 'Partial'),
        (STATUS_OVERDUE, 'Overdue')
    ]
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Student (Foreign Key)
    # Every payment is for a specific student
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Fee Structure (Foreign Key)
    # Which fee is being paid
    # RESTRICT prevents deletion if payments exist (SQLite compatible)
    fee_structure_id = db.Column(db.Integer, db.ForeignKey('fee_structure.id', ondelete='RESTRICT'), nullable=False, index=True)
    
    # Payment amount
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Payment method
    payment_method = db.Column(db.String(20), nullable=False)
    
    # Payment date (when payment was made)
    payment_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    
    # Due date (when payment was due)
    due_date = db.Column(db.Date, nullable=False, index=True)
    
    # Payment status
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDING, index=True)
    
    # Receipt number (auto-generated: RCP-YYYY-XXXXX)
    # Nullable for pending payments (no receipt yet)
    receipt_number = db.Column(db.String(50), unique=True, nullable=True, index=True)
    
    # Transaction details (for digital payments)
    # Required for Easypaisa, Jazzcash, Bank Transfer
    transaction_id = db.Column(db.String(100), unique=True, nullable=True, index=True)
    account_name = db.Column(db.String(100), nullable=True)
    
    # Group Payment (Foreign Key - for family payments)
    # If this payment is part of a family group payment
    # Nullable: Individual payments don't have group_payment_id
    group_payment_id = db.Column(db.Integer, db.ForeignKey('group_payment.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Remarks/Notes
    remarks = db.Column(db.Text, nullable=True)
    
    # Who created this payment record
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ========== RELATIONSHIPS ==========
    # One payment can have one receipt
    receipt = db.relationship('PaymentReceipt', backref='payment', uselist=False, cascade='all, delete-orphan')
    
    # ========== METHODS ==========
    
    def generate_receipt_number(self):
        """
        Generate unique receipt number
        
        Format: RCP-YYYY-XXXXX
        Example: RCP-2024-00001
        """
        from datetime import datetime
        current_year = datetime.now().year
        
        # Get the last receipt number for this year
        last_receipt = FeePayment.query.filter(
            FeePayment.receipt_number.like(f'RCP-{current_year}-%')
        ).order_by(FeePayment.receipt_number.desc()).first()
        
        if last_receipt:
            try:
                last_num = int(last_receipt.receipt_number.split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        # Format: RCP-YYYY-XXXXX
        self.receipt_number = f'RCP-{current_year}-{new_num:05d}'
    
    def update_status(self):
        """
        Update payment status based on amount and due date
        
        This is called automatically when payment is saved.
        """
        from datetime import date
        
        # If amount is 0 or negative, status is PENDING
        if self.amount <= 0:
            self.status = self.STATUS_PENDING
            return
        
        # Get the fee structure to compare amounts
        fee_amount = self.fee_structure.amount
        
        # Check if payment is complete
        if self.amount >= fee_amount:
            self.status = self.STATUS_PAID
        elif self.amount > 0:
            self.status = self.STATUS_PARTIAL
        else:
            self.status = self.STATUS_PENDING
        
        # Check if overdue
        if self.status in [self.STATUS_PENDING, self.STATUS_PARTIAL]:
            if date.today() > self.due_date:
                self.status = self.STATUS_OVERDUE
    
    def is_digital_payment(self):
        """Check if this is a digital payment (requires transaction ID)"""
        return self.payment_method in [self.PAYMENT_EASYPAISA, self.PAYMENT_JAZZCASH, self.PAYMENT_BANK_TRANSFER]
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<FeePayment {self.receipt_number or "No Receipt"} - Rs. {self.amount}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.get_full_name() if self.student else None,
            'fee_structure_id': self.fee_structure_id,
            'fee_name': self.fee_structure.fee_name if self.fee_structure else None,
            'amount': float(self.amount),
            'payment_method': self.payment_method,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'receipt_number': self.receipt_number,
            'transaction_id': self.transaction_id,
            'account_name': self.account_name
        }


# ========== EVENT LISTENER ==========
@event.listens_for(FeePayment, 'before_insert')
def generate_receipt_before_insert(mapper, connection, target):
    """Automatically generate receipt number and update status before inserting"""
    if target.status == FeePayment.STATUS_PAID and not target.receipt_number:
        target.generate_receipt_number()
    target.update_status()

@event.listens_for(FeePayment, 'before_update')
def update_status_before_update(mapper, connection, target):
    """Update status before updating"""
    target.update_status()
