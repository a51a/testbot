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
        logger.info(f"Generating fun fact for coordinates: {latitude}, {longitude}")
        
        prompt = (
            "You are a knowledgeable local guide. "
            f"A person is at coordinates {latitude}, {longitude}. "
            "Share one interesting and lesser-known fact about a place, landmark, "
            "or historical event near these coordinates. "
            "Keep it concise (max 2-3 sentences) and engaging. "
            "Focus on unique, specific details rather than general information."
        )
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable local guide."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        fact = response.choices[0].message.content.strip()
        logger.info("Successfully generated fun fact")
        return fact
        
    except openai.error.InvalidRequestError as e:
        logger.error(f"Invalid request to OpenAI: {e}")
        return "I couldn't process this location. Please try again with different coordinates."
    except openai.error.AuthenticationError as e:
        logger.error(f"Authentication error with OpenAI: {e}")
        return "There's an issue with the AI service authentication. Please try again later."
    except openai.error.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "The AI service is temporarily unavailable. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error generating fun fact: {e}")
        return "I couldn't find an interesting fact about this location at the moment. Please try again later." 