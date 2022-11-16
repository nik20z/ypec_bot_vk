from bot.database.connect import cursor, connection


table_create_queries = {
    "vkontakte": """CREATE TABLE IF NOT EXISTS vkontakte (
                                        user_id bigint NOT NULL PRIMARY KEY,
                                        user_name text,
                                        joined date,
                                        sync_code bigint REFERENCES telegram (user_id),
                                        spamming boolean DEFAULT True);"""
}


def create(table_name=None):
    """Создаём таблицу"""
    if table_name is None:
        for table_name in table_create_queries.keys():
            create(table_name=table_name)
    else:
        cursor.execute(table_create_queries.get(table_name, None))
        connection.commit()
