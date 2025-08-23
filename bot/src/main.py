import asyncio
from aiogram import Bot, Dispatcher

from bot.src.config import settings
from bot.src.handlers.admin.router import router as admin_router
from bot.src.services.database_client import DatabaseClient


async def main() -> None:
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_router)
    db_client: DatabaseClient | None = None
    try:
        if settings.DATABASE_GRPC_ADDR:
            db_client = DatabaseClient(settings.DATABASE_GRPC_ADDR)
            await db_client.start()
        await dp.start_polling(bot, skip_updates=True)
    finally:
        if db_client is not None:
            await db_client.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Start error")


