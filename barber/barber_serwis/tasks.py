from django.core.mail import EmailMessage
from celery import shared_task

@shared_task
def send_email(user, date, time):

    message = f"""Hello {user.username},
Your visit has been saved. 
Date: {date} on {time}
Thank You for being with us"""

    email = EmailMessage('Your barber visit', 
    message,
    'from@example.com', [user.email])
    return email.send()