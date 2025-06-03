import os
import sys
import logging
import re
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

def validate_token(token: str) -> bool:
    """
    Validate Telegram bot token format.
    Should be in format: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    """
    if not token:
        return False
    # Token format: numbers:letters
    pattern = r'^\d+:[\w-]+$'
    return bool(re.match(pattern, token))

def clean_token(token: str) -> str:
    """Clean the token by removing spaces and quotes"""
    if not token:
        return ""
    # Remove spaces, quotes, newlines and any hidden characters
    cleaned = token.strip().strip('"\'').strip()
    # Remove any non-alphanumeric characters except ':' and '-'
    cleaned = ''.join(c for c in cleaned if c.isalnum() or c in ':-')
    return cleaned

# Get environment variables with defaults
raw_token = os.getenv("TELEGRAM_TOKEN", "")
logger.info("Raw token length: %d", len(raw_token))
logger.info("Raw token characters: %s", ' '.join(hex(ord(c)) for c in raw_token[:10]))

TELEGRAM_TOKEN = clean_token(raw_token)
PORT = int(os.getenv("PORT", 8080))

# Validate token
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN environment variable is not set!")
    sys.exit(1)

logger.info("Cleaned token length: %d", len(TELEGRAM_TOKEN))
logger.info("Cleaned token format: %s", TELEGRAM_TOKEN[:5] + "..." + TELEGRAM_TOKEN[-5:] if len(TELEGRAM_TOKEN) > 10 else "")

if not validate_token(TELEGRAM_TOKEN):
    logger.error("Token format is invalid! Should be in format: numbers:letters")
    logger.error("Current token format: %s", TELEGRAM_TOKEN)
    sys.exit(1)

try:
    # Initialize bot and dispatcher
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(bot)
    
    # Verify bot token by making a test API call
    async def verify_token():
        try:
            me = await bot.get_me()
            logger.info(f"Bot initialized successfully. Bot username: @{me.username}")
            return True
        except Exception as e:
            logger.error(f"Failed to verify bot token: {e}")
            return False
    
    # Run token verification
    if not asyncio.run(verify_token()):
        sys.exit(1)
        
except Exception as e:
    logger.error(f"Failed to initialize bot: {e}")
    sys.exit(1)

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