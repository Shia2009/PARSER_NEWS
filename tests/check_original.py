#Проверка нет ли одних и тех же ссылок
import asyncio
import time
import sqlite3
import os

if os.name=='nt':
    path=os.path.dirname(os.path.abspath(__file__))
    DB_link=f'{path[:15]}\storage\links.db'
    print(DB_link)
elif os.name=='posix':
    path = os.path.dirname(os.path.abspath(__file__))
    DB_link=f'{path[:15]}/storage/links.db'

def tn():#time now
    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    return time_string

async def check_duplicate():
    data = []
    # работаем с БД
    print(f'[{tn()}] {DB_link} Соедениене подключено')
    conn = sqlite3.connect(DB_link)
    cursor = conn.cursor()

    # Удаляем дубликаты, оставляя запись с наименьшим ROWID
    cursor.execute(f"""
            DELETE FROM links
            WHERE rowid NOT IN (
                SELECT MIN(rowid) 
                FROM links 
                GROUP BY link
            )
        """)

    conn.commit()
    print(f"Удалено {cursor.rowcount} дубликатов")
    print(f'[{tn()}] {DB_link} Сохранение изменений')
    conn.close()
    print(f'[{tn()}] {DB_link} Соедениене закрыто')

asyncio.run(check_duplicate())