from aiogram import Bot, Dispatcher
from asyncio import run
from config import BOT_TOKEN
from database.db_init import init_db, close_db  
from handlers import router as main_router
from logging import basicConfig, INFO

basicConfig(level=INFO)

dp = Dispatcher()
dp.include_router(main_router)  

async def main():
    bot = Bot(token=BOT_TOKEN)
    try: 
        await init_db()
        await dp.start_polling(bot) 
    finally:
        await dp.stop_polling()
        await close_db()

if __name__ == "__main__":
    run(main()) 