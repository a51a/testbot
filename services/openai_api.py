import logging
import openai
from config.settings import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

async def get_fun_fact(latitude: float, longitude: float) -> str:
    """
    Generate a fun fact about a location using OpenAI's GPT model.
    
    Args:
        latitude (float): The latitude coordinate
        longitude (float): The longitude coordinate
        
    Returns:
        str: A fun fact about the location
    """
    try:
        prompt = (
            "You are a knowledgeable local guide. "
            f"A person is at coordinates {latitude}, {longitude}. "
            "Share one interesting and lesser-known fact about a place, landmark, "
            "or historical event near these coordinates. "
            "Keep it concise (max 2-3 sentences) and engaging. "
            "Focus on unique, specific details rather than general information."
        )
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",  # Using GPT-4 as GPT-4.1-mini is not available
            messages=[
                {"role": "system", "content": "You are a knowledgeable local guide."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating fun fact: {e}")
        return "I couldn't find an interesting fact about this location at the moment. Please try again later." 