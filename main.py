import os
import sys
import logging
from aiogram import Bot, Dispatcher, types
from aiohttp import web
import asyncio
from dotenv import load_dotenv
from bot.handlers import cmd_start, handle_location, handle_unknown
from services.openai_api import init_openai

# Configure logging first, before any other operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
PORT = int(os.getenv("PORT", 8080))

# Validate token
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN environment variable is not set!")
    sys.exit(1)

logger.info("Initializing bot with token length: %d", len(TELEGRAM_TOKEN))

try:
    # Initialize bot and dispatcher
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Register handlers
    @dp.message(commands=['start', 'help'])
    async def start_handler(message: types.Message):
        await cmd_start(message)

    @dp.message(content_types=['location'])
    async def location_handler(message: types.Message):
        await handle_location(message)

    @dp.message()
    async def unknown_handler(message: types.Message):
        await handle_unknown(message)

except Exception as e:
    logger.error(f"Failed to initialize bot: {e}")
    sys.exit(1)

# Web app
app = web.Application()

async def health_check(request):
    """Health check endpoint"""
    return web.Response(text="Bot is running!")

app.router.add_get("/", health_check)

async def on_startup(app):
    """Startup handler"""
    logger.info("Starting bot...")
    
    # Initialize OpenAI
    success = await init_openai()
    if not success:
        logger.error("Failed to initialize OpenAI")
    
    # Set webhook if URL is provided
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")

async def on_shutdown(app):
    """Shutdown handler"""
    logger.info("Shutting down bot...")
    await bot.session.close()

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

async def main():
    """Main function to run both bot and web server"""
    try:
        # Start web server
        logger.info(f"Starting web server on port {PORT}...")
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
        await site.start()
        
        # Start polling if no webhook URL is set
        if not os.getenv("WEBHOOK_URL"):
            logger.info("Starting polling...")
            await dp.start_polling(bot)
        else:
            logger.info("Webhook mode - not starting polling")
            
        # Keep the script running
        while True:
            await asyncio.sleep(3600)
            
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        raise
    finally:
        if 'runner' in locals():
            await runner.cleanup()

if __name__ == "__main__":
    try:
        logger.info("Starting application...")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 