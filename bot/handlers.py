import logging
from aiogram import types
from utils.location import round_coordinates
from services.openai_api import get_fun_fact

logger = logging.getLogger(__name__)

async def cmd_start(message: types.Message):
    """
    Handle /start command
    """
    logger.info(f"Received /start command from user {message.from_user.id}")
    try:
        await message.answer(
            "👋 Hi! I'm a bot that provides interesting facts about locations.\n\n"
            "To get started, simply share your location with me using the 📎 attachment menu "
            "and selecting 📍 Location.\n\n"
            "I'll tell you an interesting fact about that place!"
        )
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.answer("Sorry, something went wrong. Please try again later.")

async def handle_location(message: types.Message):
    """
    Handle incoming location messages from users.
    
    Args:
        message (types.Message): Telegram message containing location
    """
    try:
        logger.info(f"Received location from user {message.from_user.id}")
        
        if not message.location:
            await message.answer("Please share a location to get an interesting fact!")
            return

        # Send a temporary message to show we're processing
        processing_msg = await message.answer("🔍 Looking for an interesting fact about this location...")
        
        try:
            # Get coordinates
            lat = message.location.latitude
            lon = message.location.longitude
            
            # Round coordinates
            rounded_lat, rounded_lon = round_coordinates(lat, lon)
            logger.info(f"Processing location for user {message.from_user.id}: {rounded_lat}, {rounded_lon}")
            
            # Get fun fact from OpenAI
            fun_fact = await get_fun_fact(rounded_lat, rounded_lon)
            
            # Send the fun fact
            await processing_msg.edit_text(f"🌟 {fun_fact}")
            logger.info(f"Sent fact to user {message.from_user.id}")
            
        except Exception as e:
            error_msg = "Sorry, I encountered an error while processing your location. Please try again later."
            logger.error(f"Error processing location for user {message.from_user.id}: {e}")
            await processing_msg.edit_text(error_msg)
                
    except Exception as e:
        logger.error(f"Unexpected error in location handler for user {message.from_user.id}: {e}")
        try:
            await message.answer("An unexpected error occurred. Please try again later.")
        except:
            logger.error(f"Could not send error message to user {message.from_user.id}")

async def handle_unknown(message: types.Message):
    """
    Handle unknown message types
    """
    logger.info(f"Received unknown message type from user {message.from_user.id}: {message.content_type}")
    try:
        await message.answer(
            "I can only work with locations. Please share your location using the 📎 attachment menu "
            "and selecting 📍 Location."
        )
    except Exception as e:
        logger.error(f"Error in unknown handler: {e}")
        await message.answer("Sorry, something went wrong. Please try again later.") 