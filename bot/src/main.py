import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from bot.src.config import settings
from bot.src.handlers.admin.router import router as admin_router
from bot.src.services.database_client import DatabaseClient


async def _start_http_endpoints() -> web.AppRunner:
    app = web.Application()

    async def healthz(_request: web.Request) -> web.Response:
        return web.Response(text="ok")

    async def ready(_request: web.Request) -> web.Response:
        return web.Response(text="ok")

    async def metrics(_request: web.Request) -> web.Response:
        data = generate_latest()
        return web.Response(body=data, headers={"Content-Type": CONTENT_TYPE_LATEST})

    app.add_routes(
        [
            web.get("/healthz", healthz),
            web.get("/ready", ready),
            web.get("/metrics", metrics),
        ]
    )
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    return runner


async def main() -> None:
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_router)
    db_client: DatabaseClient | None = None
    http_runner: web.AppRunner | None = None
    try:
        if settings.DATABASE_GRPC_ADDR:
            db_client = DatabaseClient(settings.DATABASE_GRPC_ADDR)
            await db_client.start()
        http_runner = await _start_http_endpoints()
        await dp.start_polling(bot, skip_updates=True)
    finally:
        if db_client is not None:
            await db_client.stop()
        if http_runner is not None:
            await http_runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Start error")
