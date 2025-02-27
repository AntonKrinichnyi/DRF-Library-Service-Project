import stripe
from library_service import settings
from payment.models import Payment
from datetime import datetime, timezone

from telegram_notificated import send_telegram_notification

stripe.api_key = settings.STRIPE_SECRET_KEY

def calculate_borrowing_price(borrowing):
    num_days = (datetime.now(timezone.utc) - borrowing.borrow_date).days
    return borrowing.book.daily_fee * num_days

def create_stripe_session(borrowing):
    total_price = calculate_borrowing_price(borrowing)
    
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": borrowing.book.title,
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/payment/success/{CHECKOUT_SESSION_ID}/",
        cancel_url="http://localhost:8000/payment/cancel/",
    )
    payment = Payment.objects.create(
        status=Payment.StatusChoises.PENDING,
        payment_type=Payment.TypeChoises.PAYMENT,
        borrowing_id=borrowing,
        session_url=f"https://checkout.stripe.com/pay/{session.id}",
        session_id=session.id,
        money_to_pay=total_price,
    )
    if session.success_url:
        send_telegram_notification(
                f"Payment for rent {borrowing.id} was successful"
            )
    else:
        send_telegram_notification(
                f"Payment for rent {borrowing.id} was unsuccessful"
            )
    return payment
