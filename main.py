import asyncio
from aiogram import Bot, Dispatcher
from handlers import client, admin, vip


async def main():
    with open("token.txt", "r") as TOKEN:
        bot_token = TOKEN.readline()
    bot = Bot(bot_token)
    dp = Dispatcher()
    dp.include_routers(admin.router, vip.router, client.router)  # routers add
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("main error")
