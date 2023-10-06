import asyncio
from aiogram import Bot, Dispatcher
from handlers.client import router
json_data = "user_list.json"
push_data = "users_time.json"


async def main():
    with open("token.txt", "r") as TOKEN:
        bot_token = TOKEN.readline()
    bot = Bot("6407340014:AAFsR_mctp9ibyTYlKA7EuHoCBZamcXmw_k")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("main error")
