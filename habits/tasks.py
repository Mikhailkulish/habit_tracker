import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import Habit


@shared_task
def send_telegram_message(chat_id, text):
    """
    Отправляет сообщение в Telegram.
    Вызывается асинхронно из check_and_send_reminders.
    """
    if not chat_id:
        return "Нет chat_id (пользователь не привязал Telegram)"

    # Берем токен из настроек Django
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return "Ошибка: TELEGRAM_BOT_TOKEN не задан в настройках"

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return f"Сообщение отправлено в {chat_id}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка отправки в {chat_id}: {e}"


@shared_task
def check_and_send_reminders():
    """
    Периодическая задача (раз в минуту).
    Ищет привычки, время которых наступило, и ставит задачи на отправку.
    """
    now = timezone.localtime()

    # Определяем границы текущей минуты
    start_of_minute = now.replace(second=0, microsecond=0)
    end_of_minute = start_of_minute + timedelta(minutes=1)

    # Ищем привычки, время которых попадает в текущую минуту,
    # и у пользователя которых заполнен telegram_chat_id
    habits = Habit.objects.filter(
        time__gte=start_of_minute.time(),
        time__lt=end_of_minute.time(),
        user__telegram_chat_id__isnull=False
    ).exclude(user__telegram_chat_id='')

    count = habits.count()
    if count == 0:
        return "Нет привычек для напоминания в эту минуту"

    for habit in habits:
        text = (
            f"🔔 Напоминание!\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Время: {habit.time.strftime('%H:%M')}"
        )
        # Ставим задачу на отправку в очередь
        send_telegram_message.delay(habit.user.telegram_chat_id, text)

    return f"Поставлено в очередь напоминаний: {count}"
