import sqlite3

DB_NAME = 'weather_bot.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        city TEXT,
        notification_time TEXT
    )
    ''')
    conn.commit()
    conn.close()

def set_user_city(user_id, city):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO users (user_id, city) VALUES (?, ?)', (user_id, city))
    conn.commit()
    conn.close()

def get_user_city(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT city FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def set_notification_time(user_id, time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET notification_time = ? WHERE user_id = ?', (time, user_id))
    conn.commit()
    conn.close()

def get_notification_time(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT notification_time FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None