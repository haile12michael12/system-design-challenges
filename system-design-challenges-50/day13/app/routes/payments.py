from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional
from ..services.payment_processor import PaymentProcessor
from ..db.database import get_db
from ..workers.worker import process_payment_task

router = APIRouter()

class PaymentRequest(BaseModel):
    amount: float
    currency: str = "USD"
    payment_method: str  # "credit_card", "paypal", "bank_transfer"
    card_number: Optional[str] = None
    expiry_date: Optional[str] = None
    cvv: Optional[str] = None

class PaymentResponse(BaseModel):
    payment_id: int
    status: str
    transaction_id: Optional[str] = None
    message: str

@router.post("/payments", response_model=PaymentResponse)
async def process_payment(
    payment_request: PaymentRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """Process a payment request"""
    # In a real implementation, you would process the payment here
    # For now, we'll just queue it for background processing
    
    # Create a payment record
    payment_processor = PaymentProcessor(db)
    payment = payment_processor.create_payment(payment_request)
    
    # Queue payment for background processing
    background_tasks.add_task(process_payment_task, payment.id)
    
    return PaymentResponse(
        payment_id=payment.id,
        status="pending",
        message="Payment queued for processing"
    )

@router.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment_status(payment_id: int, db = Depends(get_db)):
    """Get the status of a payment"""
    payment_processor = PaymentProcessor(db)
    payment = payment_processor.get_payment(payment_id)
    
    if not payment:
        return PaymentResponse(
            payment_id=payment_id,
            status="not_found",
            message="Payment not found"
        )
    
    return PaymentResponse(
        payment_id=payment.id,
        status=payment.status,
        transaction_id=payment.transaction_id,
        message=f"Payment status: {payment.status}"
    )