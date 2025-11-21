from typing import List, Optional
from datetime import datetime

class Payment:
    def __init__(self, id: int, order_id: int, amount: float, currency: str, payment_method: str):
        self.id = id
        self.order_id = order_id
        self.amount = amount
        self.currency = currency
        self.payment_method = payment_method
        self.status = "pending"
        self.transaction_id = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class PaymentService:
    def __init__(self):
        # In a real implementation, this would be a database
        self.payments = {}
    
    def get_payment(self, payment_id: int) -> Optional[Payment]:
        """Get a payment by ID"""
        return self.payments.get(payment_id)
    
    def list_payments(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        """List all payments"""
        payments = list(self.payments.values())
        return payments[skip : skip + limit]
    
    def create_payment(self, order_id: int, amount: float, currency: str, payment_method: str) -> Payment:
        """Create a new payment"""
        payment_id = len(self.payments) + 1
        payment = Payment(payment_id, order_id, amount, currency, payment_method)
        self.payments[payment_id] = payment
        return payment
    
    def process_payment(self, payment_id: int) -> Optional[Payment]:
        """Process a payment"""
        payment = self.payments.get(payment_id)
        if not payment:
            return None
        
        # In a real implementation, this would integrate with a payment provider
        # For now, we'll just simulate success
        payment.status = "completed"
        payment.transaction_id = f"txn_{payment_id}"
        payment.updated_at = datetime.now()
        return payment
    
    def refund_payment(self, payment_id: int) -> Optional[Payment]:
        """Refund a payment"""
        payment = self.payments.get(payment_id)
        if not payment:
            return None
        
        payment.status = "refunded"
        payment.updated_at = datetime.now()
        return payment