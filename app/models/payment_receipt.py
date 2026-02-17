"""
Payment Receipt Model

This stores receipt information for payments.

Why this model?
- Stores receipt details separately from payment
- Can store PDF file path
- Makes it easy to regenerate receipts
- Can have different receipt formats

Note: This can represent both individual and group payment receipts.
"""

from app import db
from datetime import datetime, date


class PaymentReceipt(db.Model):
    """
    Payment Receipt Model
    
    Stores receipt information for a payment.
    Can be for individual payment or group payment.
    
    Table name: payment_receipt
    """
    
    __tablename__ = 'payment_receipt'
    
    # ========== COLUMNS (Database Fields) ==========
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Link to individual payment (One-to-One)
    # Nullable: Group payments don't have individual payment link
    payment_id = db.Column(db.Integer, db.ForeignKey('fee_payment.id', ondelete='CASCADE'), nullable=True, unique=True)
    
    # Link to group payment (One-to-One)
    # Nullable: Individual payments don't have group payment link
    group_payment_id = db.Column(db.Integer, db.ForeignKey('group_payment.id', ondelete='CASCADE'), nullable=True, unique=True)
    
    # Receipt number (same as payment receipt number)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Receipt date
    receipt_date = db.Column(db.Date, nullable=False, default=date.today)
    
    # PDF file path (if receipt is saved as PDF)
    pdf_file_path = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ========== METHODS ==========
    
    def is_group_receipt(self):
        """Check if this is a group payment receipt"""
        return self.group_payment_id is not None
    
    def get_payment(self):
        """Get the associated payment (individual or group)"""
        if self.payment_id:
            return self.payment
        elif self.group_payment_id:
            return self.group_payment
        return None
    
    def __repr__(self):
        """String representation for debugging"""
        receipt_type = "Group" if self.is_group_receipt() else "Individual"
        return f'<PaymentReceipt {receipt_type} - {self.receipt_number}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        payment = self.get_payment()
        return {
            'id': self.id,
            'receipt_number': self.receipt_number,
            'receipt_date': self.receipt_date.isoformat() if self.receipt_date else None,
            'is_group_receipt': self.is_group_receipt(),
            'pdf_file_path': self.pdf_file_path,
            'payment_details': payment.to_dict() if payment else None
        }
