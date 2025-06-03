import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from bot.handlers import handle_location
from aiohttp import web
import asyncio

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

# Create web app for health checks
app = web.Application()

async def health_check(request):
    """Health check endpoint for Railway"""
    return web.Response(text="Bot is running!")

app.router.add_get("/", health_check)

async def on_startup(dp):
    logger.info("Bot started!")

async def on_shutdown(dp):
    logger.warning("Shutting down..")
    await bot.close()

async def start_webhook():
    # Start webhook for bot
    await dp.start_polling()

if __name__ == "__main__":
    # Get the PORT from environment variable (Railway sets this)
    port = int(os.getenv("PORT", 8080))
    
    # Setup handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Create event loop
    loop = asyncio.get_event_loop()
    
    # Start both bot and web server
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    
    # Run both the bot and web server
    loop.create_task(start_webhook())
    loop.create_task(site.start())
    
    # Run forever
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(runner.cleanup())
        loop.close() 