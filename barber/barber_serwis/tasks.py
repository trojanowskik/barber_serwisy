from django.core.mail import EmailMessage
from celery import shared_task
from barber import settings

@shared_task
def send_email(user, date, time):

    message = f"""Witaj {user.username},
Twoja wizyta została zapisana. 
Data: {date} o godzinie: {time}
Dziekujemy za wsparcie!"""

    email = EmailMessage('Your barber visit', 
    message,
    settings.EMAIL_HOST_USER, [user.email])
    return email.send()