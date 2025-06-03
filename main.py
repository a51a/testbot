import os
import sys
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from bot.handlers import handle_location
from aiohttp import web
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

try:
    # Load environment variables
    load_dotenv()

    # Verify required environment variables
    required_vars = ['TELEGRAM_TOKEN', 'OPENAI_API_KEY', 'PORT']
    for var in required_vars:
        value = os.getenv(var)
        if var == 'PORT':
            value = value or '8080'  # Default port if not set
        if not value and var != 'PORT':
            raise ValueError(f"Missing required environment variable: {var}")
        logger.info(f"Environment variable {var} is set")

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
        await bot.send_message(chat_id=os.getenv('ADMIN_CHAT_ID', ''), text="Bot has been started!")

    async def on_shutdown(dp):
        logger.warning("Shutting down..")
        await bot.close()

    async def start_bot():
        try:
            await dp.start_polling()
        except Exception as e:
            logger.error(f"Error in bot polling: {e}")
            raise

    if __name__ == "__main__":
        # Get the PORT from environment variable (Railway sets this)
        port = int(os.getenv("PORT", 8080))
        logger.info(f"Starting server on port {port}")
        
        # Setup handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Create event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Start both bot and web server
            runner = web.AppRunner(app)
            loop.run_until_complete(runner.setup())
            site = web.TCPSite(runner, host="0.0.0.0", port=port)
            
            # Run both the bot and web server
            loop.create_task(start_bot())
            loop.create_task(site.start())
            
            # Run forever
            logger.info("Starting event loop")
            loop.run_forever()
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            sys.exit(1)
        finally:
            try:
                loop.run_until_complete(runner.cleanup())
                loop.close()
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
except Exception as e:
    logger.error(f"Initialization error: {e}")
    sys.exit(1) 