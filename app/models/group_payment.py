"""
Group Payment Model

This represents a family/group payment where multiple students (siblings) pay together.

Why this model?
- Parents with multiple children want to pay all fees in one transaction
- One receipt for all siblings instead of separate receipts
- Better organization and tracking
- Faster payment processing

Example:
- Family: Muhammad Ahmed Khan
- Children: Ahmed (Rs. 5,000), Ali (Rs. 4,000), Fatima (Rs. 3,500)
- Total: Rs. 12,500 in one payment
- One receipt: GP-2024-00001
"""

from app import db
from datetime import datetime, date
from sqlalchemy import event


class GroupPayment(db.Model):
    """
    Group Payment Model
    
    Represents a payment made for multiple students (siblings) in a single transaction.
    Links to multiple FeePayment records.
    Has its own receipt number.
    
    Table name: group_payment
    """
    
    __tablename__ = 'group_payment'
    
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
    
    # ========== STATUS ==========
    STATUS_PAID = 'PAID'
    STATUS_PARTIAL = 'PARTIAL'
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Group Payment Number (unique identifier, auto-generated: GP-YYYY-XXXXX)
    # Format: GP-2024-00001
    group_payment_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Family (Foreign Key)
    # Which family made this payment
    family_id = db.Column(db.Integer, db.ForeignKey('family.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Total amount (sum of all individual payments)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Payment method
    payment_method = db.Column(db.String(20), nullable=False)
    
    # Payment date
    payment_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    
    # Transaction details (for digital payments)
    transaction_id = db.Column(db.String(100), unique=True, nullable=True, index=True)
    account_name = db.Column(db.String(100), nullable=True)
    
    # Receipt number (single receipt for all students)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Payment status
    status = db.Column(db.String(20), nullable=False, default=STATUS_PAID)
    
    # Number of students in this payment
    students_count = db.Column(db.Integer, nullable=False, default=0)
    
    # Who created this payment record
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ========== RELATIONSHIPS ==========
    # One group payment can have many individual fee payments
    fee_payments = db.relationship('FeePayment', backref='group_payment', lazy='dynamic')
    
    # One group payment can have one receipt
    receipt = db.relationship('PaymentReceipt', backref='group_payment', uselist=False, cascade='all, delete-orphan')
    
    # ========== METHODS ==========
    
    def generate_group_payment_number(self):
        """
        Generate unique group payment number
        
        Format: GP-YYYY-XXXXX
        Example: GP-2024-00001
        """
        from datetime import datetime
        current_year = datetime.now().year
        
        # Get the last group payment number for this year
        last_payment = GroupPayment.query.filter(
            GroupPayment.group_payment_number.like(f'GP-{current_year}-%')
        ).order_by(GroupPayment.group_payment_number.desc()).first()
        
        if last_payment:
            try:
                last_num = int(last_payment.group_payment_number.split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        # Format: GP-YYYY-XXXXX
        self.group_payment_number = f'GP-{current_year}-{new_num:05d}'
    
    def generate_receipt_number(self):
        """
        Generate unique receipt number for group payment
        
        Uses the same format as individual receipts (RCP-YYYY-XXXXX) for consistency
        """
        from datetime import datetime
        from sqlalchemy import func
        current_year = datetime.now().year
        
        # Get the last receipt number from FeePayment table
        from app.models.fee_payment import FeePayment
        last_fp = db.session.query(func.max(FeePayment.receipt_number)).filter(
            FeePayment.receipt_number.like(f'RCP-{current_year}-%')
        ).scalar()
        
        # Get the last receipt number from GroupPayment table
        last_gp = db.session.query(func.max(GroupPayment.receipt_number)).filter(
            GroupPayment.receipt_number.like(f'RCP-{current_year}-%')
        ).scalar()
        
        # Get the maximum of both (or None if both are None)
        last_receipt = None
        if last_fp and last_gp:
            last_receipt = max(last_fp, last_gp)
        elif last_fp:
            last_receipt = last_fp
        elif last_gp:
            last_receipt = last_gp
        
        if last_receipt:
            try:
                last_num = int(last_receipt.split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        # Format: RCP-YYYY-XXXXX (same as individual receipts)
        self.receipt_number = f'RCP-{current_year}-{new_num:05d}'
    
    def calculate_total(self):
        """Calculate total amount from associated fee payments"""
        total = sum(float(payment.amount) for payment in self.fee_payments.all())
        self.total_amount = total
        self.students_count = self.fee_payments.count()
        return total
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<GroupPayment {self.group_payment_number} - Rs. {self.total_amount}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'group_payment_number': self.group_payment_number,
            'family_code': self.family.family_code if self.family else None,
            'father_name': self.family.father_name if self.family else None,
            'total_amount': float(self.total_amount),
            'payment_method': self.payment_method,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'receipt_number': self.receipt_number,
            'status': self.status,
            'students_count': self.students_count,
            'fee_payments': [fp.to_dict() for fp in self.fee_payments.all()]
        }


# ========== EVENT LISTENER ==========
@event.listens_for(GroupPayment, 'before_insert')
def generate_numbers_before_insert(mapper, connection, target):
    """Automatically generate payment number and receipt number before inserting"""
    if not target.group_payment_number:
        target.generate_group_payment_number()
    if not target.receipt_number:
        target.generate_receipt_number()
