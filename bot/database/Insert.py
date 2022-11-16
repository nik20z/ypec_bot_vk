from bot.database.connect import cursor, connection


def new_user(data_: tuple):
    """Добавляем нового пользователя"""
    cursor.execute("INSERT INTO vkontakte (user_id, user_name, joined) VALUES (%s, %s, %s)", data_)
    connection.commit()
