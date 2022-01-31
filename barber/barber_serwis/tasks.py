from django.core.mail import EmailMessage
from celery import shared_task

@shared_task
def send_email(user, date, time):

    message = f"""Witaj {user.username},
Twoja wizyta została zapisana. 
Data: {date} o godzinie: {time}
Dziekujemy za wsparcie!"""

    email = EmailMessage('Your barber visit', 
    message,
    'from@example.com', [user.email])
    return email.send()