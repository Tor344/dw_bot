import aiosqlite

async def creation():
    # Устанавливаем соединение с базой данных
    async with aiosqlite.connect('my_database.db') as db:
        cursor = await db.cursor()

        # Создаем таблицу Users
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY
        )
        ''')

        # Создаем таблицу Channels
        await cursor.execute('''
                CREATE TABLE IF NOT EXISTS Channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
                ''')

        # Сохраняем изменения
        await db.commit()


async def add_user_if_not_exists(user_id: int):
    """
    Добавляет пользователя в таблицу Users, если его там нет.
    :param user_id: ID пользователя.
    """
    async with aiosqlite.connect('my_database.db') as db:
        cursor = await db.cursor()

        # Добавляем пользователя, если его нет
        await cursor.execute('''
        INSERT OR IGNORE INTO Users (id) VALUES (?)
        ''', (user_id,))

        # Сохраняем изменения
        await db.commit()


async def add_channel(channel_name):
    """
    Добавляет канал в таблицу Channels.
    Если канал с таким именем уже существует, ничего не делает.
    """
    async with aiosqlite.connect('my_database.db') as db:
        cursor = await db.cursor()

        # Проверяем, существует ли канал с таким именем
        await cursor.execute("SELECT 1 FROM Channels WHERE name = ?", (channel_name,))
        channel = await cursor.fetchone()

        # Если канала нет, добавляем его
        if not channel:
            await cursor.execute("INSERT INTO Channels (name) VALUES (?)", (channel_name,))
            await db.commit()
            return True  # Канал добавлен
        return False  # Канал уже существует


async def delete_channel(channel_name):
    """
    Удаляет канал из таблицы Channels по его имени.
    :param channel_name: Имя канала для удаления.
    :return: 1, если канал удален, 0, если канал не найден.
    """
    async with aiosqlite.connect('my_database.db') as db:
        cursor = await db.cursor()

        # Удаляем канал
        await cursor.execute("DELETE FROM Channels WHERE name = ?", (channel_name,))
        await db.commit()

        # Возвращаем 1, если канал удален, иначе 0
        return 1 if cursor.rowcount > 0 else 0



async def get_all_channels():
    """
    Возвращает список всех каналов из таблицы Channels.
    """
    async with aiosqlite.connect('my_database.db') as db:
        cursor = await db.cursor()

        # Получаем все каналы
        await cursor.execute("SELECT name FROM Channels")
        channels = await cursor.fetchall()

        # Возвращаем список имен каналов
        return [channel[0] for channel in channels]


async def get_user_count():
    """
    Возвращает количество пользователей в таблице Users.
    """
    async with aiosqlite.connect('my_database.db') as db:
        cursor = await db.cursor()

        # Выполняем запрос для подсчета пользователей
        await cursor.execute("SELECT COUNT(*) FROM Users")
        result = await cursor.fetchone()

        # Возвращаем количество пользователей
        return result[0] if result else 0