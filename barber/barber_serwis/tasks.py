from django.core.mail import EmailMessage
from celery import shared_task

@shared_task
def send_email(user, data):
    date, time = data['date'].split('T')
    time = time.split(':')[:2]
    time = ':'.join(time)

    message = f"""Hello {user.username},
Your visit has been saved. 
Date: {date} on {time}
Thank You for being with us"""

    email = EmailMessage('Your barber visit', 
    message,
    'from@example.com', [user.email])
    return email.send()