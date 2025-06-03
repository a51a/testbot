import os
import sys
import logging
from aiogram import Bot, Dispatcher, types
from aiohttp import web
import asyncio
from dotenv import load_dotenv
from bot.handlers import handle_location

# Configure logging first, before any other operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get environment variables with defaults
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 8080))

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN environment variable is not set!")
    sys.exit(1)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Register handlers
@dp.message_handler(content_types=[types.ContentType.LOCATION])
async def location_handler(message: types.Message):
    await handle_location(message)

# Web app
app = web.Application()

async def health_check(request):
    """Health check endpoint"""
    return web.Response(text="Bot is running!")

app.router.add_get("/", health_check)

async def start_bot():
    """Start the bot polling"""
    logger.info("Starting bot polling...")
    await dp.start_polling()

async def start_web():
    """Start the web server"""
    logger.info(f"Starting web server on port {PORT}...")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
    await site.start()
    return runner

async def main():
    """Main function to run both bot and web server"""
    try:
        # Start web server
        runner = await start_web()
        
        # Start bot
        await start_bot()
        
        # Keep the script running
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour
            
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        raise
    finally:
        if 'runner' in locals():
            await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 