import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot,Dispatcher

from app.handlers import router

load_dotenv()
api_key = os.getenv('API_TOKEN')

bot = Bot(token=api_key)
dp = Dispatcher()


async def main():

    dp.include_router(router)
    await asyncio.gather(dp.start_polling(bot))



if __name__ == "__main__":
    asyncio.run(main())
