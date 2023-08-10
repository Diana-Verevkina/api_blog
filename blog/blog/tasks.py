from celery import shared_task
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datetime import datetime, timedelta


@shared_task
def send_daily_emails():
    # Получите всех пользователей
    users = User.objects.all()

    # Отправьте письмо каждому пользователю
    for user in users:
        subject = 'Ежедневное письмо'
        message = 'Привет, {}! Это ваше ежедневное письмо.'.format(
            user.username)
        from_email = 'diva2208@mail.ru'  # Укажите отправителя
        to_email = [user.email]

        email = EmailMessage(subject, message, from_email, to_email)
        email.send()

    # Запланируйте задачу на следующий день
    tomorrow = datetime.now() + timedelta(days=1)
    send_daily_emails.apply_async(
        eta=tomorrow.replace(hour=0, minute=0, second=0, microsecond=0))
