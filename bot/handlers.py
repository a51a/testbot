import logging
from aiogram import types
from utils.location import round_coordinates

logger = logging.getLogger(__name__)

async def handle_location(message: types.Message):
    """
    Handle incoming location messages from users.
    
    Args:
        message (types.Message): Telegram message containing location
    """
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        rounded_lat, rounded_lon = round_coordinates(lat, lon)
        
        logger.info(f"Received location: {rounded_lat}, {rounded_lon}")
        
        # TODO: Integrate with OpenAI to get fun fact
        await message.reply("Thanks for sharing your location! Fun fact coming soon...") 