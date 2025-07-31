import asyncio
import time
from parser.core import main_core
from tests.check_original import check_duplicate
from tests.backup import backup, main_backup


async def main():
    await main_core()
    await check_duplicate()
    await backup()
    await main_backup()
    await asyncio.sleep(60)

while __name__=='__main__':
    asyncio.run(main())