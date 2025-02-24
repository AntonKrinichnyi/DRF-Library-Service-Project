from datetime import datetime
from celery import shared_task
from borrowing.models import Borrowing
from telegram_notificated import send_telegram_notification


@shared_task
def borrowing_overdue_message():
    overdue_borrowings = Borrowing.objects.filter(
        expected_return__lt=datetime.now(), actual_return__isnull=True
    )

    if overdue_borrowings:
        for borrowing in overdue_borrowings:
            send_telegram_notification(
                f"User {borrowing.user.email}, you have overdue\
                    borrowing with book {borrowing.book.title}"
            )
    else:
        send_telegram_notification("No overdue borrowing")
