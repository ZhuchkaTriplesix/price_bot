import asyncio
from aiogram import Bot, Dispatcher

from bot.src.config import settings
from bot.src.handlers import admin_router


async def main() -> None:
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Start error")


