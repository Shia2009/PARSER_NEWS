#главная мысль. Cбор парсеров. Сбор всех ссылок.
from bbc_parser import bbc_links
from rbc_parser import rbc_links
from habr_parser import habr_links
import asyncio

links={'bbc':'https://www.bbc.com/russian/articles/', 'rbc':'https://www.rbc.ru/', 'habr':'https://habr.com/ru/news/'}
content=[]

async def all_links():
    content.append(await bbc_links(links["bbc"]))
    content.append(await rbc_links(links["rbc"]))
    content.append(await habr_links(links["habr"]))
    for i, news in enumerate(content):
        print(f'{i}. {news}')

# Запуск асинхронного кода
asyncio.run(all_links())