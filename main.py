import asyncio
from aiogram import Bot, Dispatcher
from handlers import client, admin, vip
from core.config import settings


async def main():
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    dp.include_routers(admin.router, vip.router, client.router)  # routers add
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Start error")
