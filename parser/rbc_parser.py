#парсер для парсинга РБК. Ссылки хронятся в links
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin


async def rbc_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    async with (aiohttp.ClientSession(headers=headers) as session):
        try:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    base_url = str(response.url)  # Получаем базовый URL для относительных ссылок
                    links = set()  # Используем set для исключения дубликатов
                    for link in soup.find_all('a', href=True):
                        href = link['href'].strip()
                        if href and href.startswith(('https://www.rbc.ru/society/', 'https://www.rbc.ru/politics/', 'https://www.rbc.ru/demo/')) and not href.endswith(('?utm_source=topline','/')):
                            links.add(href)

                    return sorted(links)
                else:
                    print(f"Ошибка {response.status} для {url}")
                    return []
        except Exception as e:
            print(f"Ошибка при запросе {url}: {e}")
            return []


async def main():
    url = "https://www.rbc.ru/"  # Замените на нужный URL
    links = await rbc_links(url)

    print(f"Найдено {len(links)} ссылок на {url}:")
    for i, link in enumerate(links):
        print(f"{i}. {link}")

if __name__ == '__main__':
    asyncio.run(main())