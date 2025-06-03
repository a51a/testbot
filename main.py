import os
import logging
from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)

if __name__ == "__main__":
    logger.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True) 