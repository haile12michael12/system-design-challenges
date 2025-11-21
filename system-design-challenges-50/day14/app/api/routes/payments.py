from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    currency: str = "USD"
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    status: str
    transaction_id: Optional[str]
    created_at: datetime
    updated_at: datetime

# Mock data storage
payments = []

@router.get("/", response_model=list[Payment])
async def list_payments(skip: int = 0, limit: int = 100):
    """List all payments"""
    return payments[skip : skip + limit]

@router.post("/", response_model=Payment)
async def create_payment(payment: PaymentCreate):
    """Create a new payment"""
    new_payment = Payment(
        id=len(payments) + 1,
        **payment.dict(),
        status="pending",
        transaction_id=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    payments.append(new_payment)
    return new_payment

@router.get("/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int):
    """Get a payment by ID"""
    for payment in payments:
        if payment.id == payment_id:
            return payment
    return {"error": "Payment not found"}

@router.put("/{payment_id}/complete", response_model=Payment)
async def complete_payment(payment_id: int):
    """Complete a payment"""
    for payment in payments:
        if payment.id == payment_id:
            payment.status = "completed"
            payment.transaction_id = f"txn_{payment_id}"
            payment.updated_at = datetime.now()
            return payment
    return {"error": "Payment not found"}