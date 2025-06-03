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
    try:
        if not message.location:
            await message.reply("Please share a location to get an interesting fact!")
            return

        # Send a temporary message to show we're processing
        processing_msg = await message.reply("🔍 Looking for an interesting fact about this location...")
        
        try:
            # Get coordinates
            lat = message.location.latitude
            lon = message.location.longitude
            
            # Round coordinates
            rounded_lat, rounded_lon = round_coordinates(lat, lon)
            logger.info(f"Processing location: {rounded_lat}, {rounded_lon}")
            
            # Get fun fact from OpenAI
            fun_fact = await get_fun_fact(rounded_lat, rounded_lon)
            
            # Edit the temporary message with the fun fact
            await processing_msg.edit_text(f"🌟 {fun_fact}")
            
        except Exception as e:
            error_msg = "Sorry, I encountered an error while processing your location. Please try again later."
            logger.error(f"Error processing location: {e}")
            
            try:
                await processing_msg.edit_text(error_msg)
            except Exception as edit_error:
                logger.error(f"Could not edit processing message: {edit_error}")
                await message.reply(error_msg)
                
    except Exception as e:
        logger.error(f"Unexpected error in location handler: {e}")
        try:
            await message.reply("An unexpected error occurred. Please try again later.")
        except:
            logger.error("Could not send error message to user") 