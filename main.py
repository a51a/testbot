import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from bot.handlers import handle_location

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)

# Register handlers
dp.register_message_handler(handle_location, content_types=[types.ContentType.LOCATION])

if __name__ == "__main__":
    logger.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True) 