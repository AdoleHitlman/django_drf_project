from django.contrib.auth.models import User
from django.utils import timezone
import smtplib
from email.mime.text import MIMEText
from celery import shared_task

from lesson_manage.models import Course

@shared_task
def block_inactive_users():
    # Получаем текущую дату и время
    current_time = timezone.now()

    # Получаем всех пользователей
    users = User.objects.all()

    # Перебираем пользователей и проверяем дату последнего входа
    for user in users:
        # Разница между текущим временем и датой последнего входа пользователя
        time_difference = current_time - user.last_login

        # Если разница больше чем 30 дней (1 месяц), блокируем пользователя
        if time_difference.days >= 30:
            user.is_active = False
            user.save()

    return 'Background task completed successfully!'
def get_users_with_course_updates():
    updated_courses = Course.objects.filter(is_updated=True)
    users = User.objects.filter(courses__in=updated_courses)
    return users

@shared_task
def send_email(recipient, subject, message):
    # Замените нижеприведенные данные на свои данные электронной почты
    sender_email = 'matveiplitchenko@yandex.ru'
    sender_password = 'ovckrxtxnetfjrkc'

    # Создание MIME-сообщения
    mime_message = MIMEText(message, 'plain')
    mime_message['Subject'] = subject
    mime_message['From'] = sender_email
    mime_message['To'] = recipient

    # Подключение к серверу SMTP и отправка письма
    with smtplib.SMTP_SSL(' smtp.yandex.ru', 465) as smtp_server:
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipient, mime_message.as_string())

# Задача Celery для отправки обновлений по электронной почте
@shared_task
def send_update_emails():
    users = get_users_with_course_updates()
    for user in users:
        recipient = user.email
        subject = 'Обновление материалов курса'
        message = 'Привет, {}. В курсе, на который вы подписаны, были добавлены новые материалы.'.format(user.name)
        send_email(recipient, subject, message)