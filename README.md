# Погодный Telegram бот

Этот Telegram бот предоставляет информацию о погоде и позволяет настраивать ежедневные уведомления.

## Функции

1. **/start** - Начать общение с ботом и открыть главное меню.
2. **/set_city** - Установить город для получения информации о погоде.
3. **/weather** - Получить текущую погоду в установленном городе.
4. **/set_notification** - Установить ежедневное уведомление о погоде.

## Как использовать

1. **Установка Python и зависимостей**
   - Установите Python 3.7+.
   - Установите необходимые библиотеки с помощью команды:
     ```
     pip install -r requirements.txt
     ```

2. **Настройка бота**
   - Создайте нового бота через [BotFather](https://t.me/BotFather) в Telegram и получите токен.
   - Вставьте полученный токен в переменную `TOKEN` в файле `main.py`.

3. **Запуск бота**
   - Запустите бота с помощью команды:
     ```
     python main.py
     ```
   - Теперь бот готов к использованию. Начните диалог с ботом, отправив команду /start.

## Дополнительные настройки

- Вы можете настроить локализацию бота, изменив языковой код в методе `Updater` в файле `main.py`.
- Для дополнительной функциональности или настройки обработчиков команд и сообщений, редактируйте соответствующие функции в файле `main.py`.
