#главная мысль. Cбор парсеров. Сбор всех ссылок.
import sqlite3
from parser.bbc_parser import bbc_links
from parser.rbc_parser import rbc_links
from parser.habr_parser import habr_links
import asyncio
import time
import os


links={'bbc':'https://www.bbc.com/russian/articles/', 'rbc':'https://www.rbc.ru/', 'habr':'https://habr.com/ru/news/'}
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

async def main_core():
    #собираем ссылки
    content = []
    for i in await bbc_links(links["bbc"]):
        content.append(i)
    for i in await rbc_links(links["rbc"]):
        content.append(i)
    for i in await habr_links(links["habr"]):
        content.append(i)
    print(f'[{tn()}] Ссылки полученны и собранны')

    #работаем с БД
    print(f'[{tn()}] {DB_link} Соедениене подключено')
    conn = sqlite3.connect(DB_link)
    cursor= conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS links
                      (id INTEGER PRIMARY KEY, link TEXT, time TEXT)''')
    for i, news in enumerate(content):
        named_tuple = time.localtime()  # получаем struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        parametes=(str(news), str(time_string))
        cursor.execute("INSERT INTO links (link, time) VALUES (?, ?)", parametes)
        print(f'[{time_string}] {DB_link} Записано <<{news}>>, <<{time_string}>>')
    conn.commit()
    print(f'[{tn()}] {DB_link} Сохранение изменений')
    conn.close()
    print(f'[{tn()}] {DB_link} Соедениене закрыто')


# Запуск асинхронного кода
asyncio.run(main_core())