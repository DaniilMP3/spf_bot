import sqlite3
from create_bot import USERS


async def update_or_create_user(data): ### if user in db - update
    connection = sqlite3.connect('database.db')

    with connection:
        cursor = connection.cursor()
        user_id = data[0]
        res = await get_user(user_id)
        if res:
            data = data[1:len(data) - 1] ### remove meetings count and id fields field from data if user exists in db
            cursor.execute(f'UPDATE user SET full_name = ?, sex = ?, speciality = ?, grade = ?, user_group = ? WHERE user_id = {user_id}', data)
            connection.commit()
            return
        cursor.execute('INSERT INTO user VALUES(?,?,?,?,?,?,?)', data)

        connection.commit()


async def get_user(user_id):
    connection = sqlite3.connect('database.db')

    with connection:
        cursor = connection.cursor()
        res = cursor.execute(f'SELECT * FROM user WHERE user_id = {user_id}')

    if res is None:
        return False

    return res.fetchone()


def get_all_users():
    connection = sqlite3.connect('database.db')

    with connection:
        cursor = connection.cursor()
        res = cursor.execute('SELECT * FROM user')
    for i in res:
        user_id, full_name, sex, speciality, grade, user_group, meetings_count = i[0], i[1], i[2], i[3], i[4], i[5], i[6]
        USERS[user_id] = {'full_name': full_name, 'sex': sex,
                          'speciality': speciality, 'grade': grade,
                          'user_group': user_group, 'meetings_count': meetings_count}

    return res.fetchall()


async def create_meeting(first_user_id, second_user_id, time):
    async def get_time():
        nonlocal res
        import datetime

        pass


    connection = sqlite3.connect('database.db')

    with connection:
        cursor = connection.cursor()
        # cursor.execute('CREATE TABLE IF NOT EXISTS meeting(first_user_id VARCHAR NOT NULL, second_user_id VARCHAR NOT NULL, time TEXT NOT NULL, link INTEGER NOT NULL, FOREIGN KEY(link) REFERENCES link(id))')
        res = cursor.execute('SELECT * FROM meeting')
        if res is None:
            pass



        connection.commit()