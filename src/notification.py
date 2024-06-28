from telegram.ext import CallbackContext
from src.database import get_user_city, set_notification_time, delete_notification_time
from src.weather import get_weather
import datetime

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def set_daily_notification(context: CallbackContext, user_id: int, time: str) -> None:
    hour, minute = map(int, time.split(':'))

    # Запускаем ежедневное уведомление
    context.job_queue.run_daily(send_weather_update, time=datetime.time(hour, minute), data=user_id, name=str(user_id))

    # Сохраняем время уведомления для пользователя
    set_notification_time(user_id, time)

    # Отправляем сообщение пользователю о успешной установке уведомления
    context.bot.send_message(user_id, text=f'Ежедневное уведомление о погоде успешно установлено на {time}')

async def send_weather_update(context: CallbackContext) -> None:
    job = context.job
    user_id = job.data
    city = get_user_city(user_id)
    if city:
        weather_data = get_weather(city)
        if weather_data:
            description, temp, uv_index = weather_data
            advice = "Сегодня солнечно! Наносите SPF." if uv_index > 3 else "Сегодня УФ-индекс низкий. SPF не требуется."
            await context.bot.send_message(user_id, text=f'Погода в {city}: {description}, {temp}°C, УФ-индекс: {uv_index}. {advice}')
        else:
            await context.bot.send_message(user_id, text='Не удалось получить данные о погоде. Попробуйте позже.')
    else:
        await context.bot.send_message(user_id, text='Сначала установите ваш город с помощью команды "Указать город".')

async def remove_daily_notification(context: CallbackContext, user_id: int) -> None:
    job_removed = remove_job_if_exists(str(user_id), context)
    if job_removed:
        delete_notification_time(user_id)
        await context.bot.send_message(user_id, text='Ежедневное уведомление было успешно удалено.')
    else:
        await context.bot.send_message(user_id, text='У вас нет активного ежедневного уведомления.')


