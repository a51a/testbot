import logging
from aiogram import types
from utils.location import round_coordinates
from services.openai_api import get_fun_fact

logger = logging.getLogger(__name__)

async def handle_location(message: types.Message):
    """
    Handle incoming location messages from users.
    
    Args:
        message (types.Message): Telegram message containing location
    """
    if message.location:
        # Send a temporary message to show we're processing
        processing_msg = await message.reply("🔍 Looking for an interesting fact about this location...")
        
        try:
            lat = message.location.latitude
            lon = message.location.longitude
            rounded_lat, rounded_lon = round_coordinates(lat, lon)
            
            logger.info(f"Received location: {rounded_lat}, {rounded_lon}")
            
            # Get fun fact from OpenAI
            fun_fact = await get_fun_fact(rounded_lat, rounded_lon)
            
            # Edit the temporary message with the fun fact
            await processing_msg.edit_text(f"🌟 {fun_fact}")
            
        except Exception as e:
            logger.error(f"Error processing location: {e}")
            await processing_msg.edit_text("Sorry, I encountered an error while processing your location. Please try again later.") 