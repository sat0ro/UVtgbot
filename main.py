import logging
import asyncio
import nest_asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from src.weather import get_weather
from src.database import init_db, set_user_city, get_user_city, set_notification_time
from src.notification import remove_job_if_exists, set_daily_notification

TOKEN = '849815581:AAEi6nWb6XFX_-hjLQ6WlU4GQlc4O0JOwBc'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Инициализация базы данных
init_db()

nest_asyncio.apply()
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [['Указать город', 'Погода и индекс УФ'], ['Установить напоминание']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text('Привет! Я погодный бот. Выберите команду:', reply_markup=reply_markup)

async def set_city(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Пожалуйста, введите название вашего города:')
    # Сохраняем состояние, что пользователь в процессе установки города
    context.user_data['Указать город'] = True

async def weather(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    city = get_user_city(user_id)
    if city:
        weather_data = get_weather(city)
        if weather_data:
            description, temp, uv_index = weather_data
            await update.message.reply_text(f'Погода в {city}: {description}, {temp}°C, УФ-индекс: {uv_index}')
        else:
            await update.message.reply_text('Не удалось получить данные о погоде. Попробуйте позже.')
    else:
        await update.message.reply_text('Сначала установите ваш город с помощью команды "Указать город"')

async def set_notification(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Пожалуйста, введите время для ежедневного уведомления (формат 00:00):')
    # Сохраняем состояние, что пользователь в процессе установки уведомления
    context.user_data['Установить напоминание'] = True

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    text = update.message.text

    if 'Указать город' in context.user_data:
        set_user_city(user_id, text)
        await update.message.reply_text(f'Город установлен на {text}')
        context.user_data.pop('Указать город')
    elif 'Установить напоминание' in context.user_data:
        try:
            set_notification_time(user_id, text)
            job_removed = remove_job_if_exists(str(user_id), context)
            set_daily_notification(context, user_id, text)
            text = f'Уведомление установлено на {text}.'
            if job_removed:
                text += ' Старое задание было удалено.'
            await update.message.reply_text(text)
            context.user_data.pop('Установить напоминание')
        except ValueError:
            await update.message.reply_text('Неверный формат времени. Пожалуйста, используйте формат 00:00.')

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('^(Указать город)$'), set_city))
    application.add_handler(MessageHandler(filters.Regex('^(Погода и индекс УФ)$'), weather))
    application.add_handler(MessageHandler(filters.Regex('^(Установить напоминание)$'), set_notification))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())