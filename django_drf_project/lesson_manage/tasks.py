from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone

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

@shared_task
def send_updates():
    pass