#делает бэкапы каждые 5 мин и удаляет бэкапы которым более 10 мин
import shutil
import asyncio
import os
import time
import random
import string
from datetime import datetime, timedelta
import platform
import logging

def lowercase_random_string(length=5):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def tn():#time now
    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%H:%M:%S", named_tuple)
    return time_string

if os.name=='nt':
    path=os.path.dirname(os.path.abspath(__file__))
    DB_link=f'{path[:15]}\storage\links.db'
    DB_link_new=fr'{path[:15]}\storage\backups\{lowercase_random_string()}_link.db'
    DB_link_path = fr'{path[:15]}\storage\backups'
elif os.name=='posix':
    path = os.path.dirname(os.path.abspath(__file__))
    DB_link=f'{path[:15]}/storage/links.db'
    DB_link_new=f'{path[:15]}/storage/backups/{lowercase_random_string()}_link.db'
    DB_link_path=f'{path[:15]}/storage/backups'

async def backup():
    shutil.copy(f'{DB_link}', f'{DB_link_new}')
    await asyncio.sleep(120)


import os
import asyncio
import platform
import logging
from datetime import datetime, timedelta
import aiofiles.os as aios  # Асинхронные файловые операции


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('file_cleanup.log'),
            logging.StreamHandler()
        ]
    )


async def get_file_creation_time(path):
    """Асинхронное получение времени создания файла с учетом ОС"""
    if platform.system() == 'Windows':
        stat = await aios.stat(path)
        return stat.st_ctime
    else:
        stat = await aios.stat(path)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


async def process_file(file_path, max_age_seconds, current_time):
    """Асинхронная обработка одного файла"""
    try:
        if await aios.path.isfile(file_path):
            creation_time = await get_file_creation_time(file_path)
            file_age = current_time - creation_time

            if file_age > max_age_seconds:
                try:
                    await aios.remove(file_path)
                    logging.info(f"Удален: {os.path.basename(file_path)} (возраст: {file_age / 60:.1f} минут)")
                    return True
                except Exception as e:
                    logging.error(f"Ошибка удаления {file_path}: {str(e)}")
                    return False
        return False
    except Exception as e:
        logging.error(f"Ошибка обработки файла {file_path}: {str(e)}")
        return False


async def cleanup_old_files(directory, max_age_minutes=10):
    """Асинхронное удаление файлов старше указанного возраста"""
    current_time = time.time()
    max_age_seconds = max_age_minutes * 60
    deleted_count = 0
    error_count = 0

    logging.info(f"Начало асинхронной очистки в директории: {directory}")

    try:
        files = await aios.listdir(directory)
        tasks = []

        for filename in files:
            file_path = os.path.join(directory, filename)
            task = asyncio.create_task(process_file(file_path, max_age_seconds, current_time))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        deleted_count = sum(1 for result in results if result is True)
        error_count = sum(1 for result in results if isinstance(result, Exception))

    except Exception as e:
        logging.error(f"Ошибка доступа к директории: {str(e)}")
        return False

    logging.info(f"Завершено. Удалено файлов: {deleted_count}, ошибок: {error_count}")
    return True


async def main_backup():
    setup_logging()
    target_directory = DB_link_path  # Укажите вашу директорию

    # Асинхронные проверки
    if not await aios.path.exists(target_directory):
        logging.error(f"Директория не существует: {target_directory}")
        return

    if not await aios.path.isdir(target_directory):
        logging.error(f"Указанный путь не является директорией: {target_directory}")
        return

    await cleanup_old_files(target_directory)


if __name__ == "__main__":
    asyncio.run(main_backup())
    asyncio.run(backup())