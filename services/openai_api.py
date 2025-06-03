import logging
import os
from openai import AsyncOpenAI
from config.settings import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# Initialize AsyncOpenAI client
client = None

def init_openai():
    """Initialize OpenAI with API key and verify access"""
    global client
    
    # Check if running on Railway
    is_railway = bool(os.getenv('RAILWAY_ENVIRONMENT'))
    logger.info(f"Running on Railway: {is_railway}")
    
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key is not set in environment!")
        logger.info("Environment variables available: %s", list(os.environ.keys()))
        return False
        
    try:
        # Configure OpenAI client with just the API key
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        # Log partial key for debugging (safely)
        key_start = OPENAI_API_KEY[:5] if len(OPENAI_API_KEY) > 8 else "****"
        key_end = OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 8 else "****"
        logger.info(f"Initialized OpenAI with API key: {key_start}...{key_end}")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing OpenAI client: {str(e)}")
        return False

# Initialize OpenAI when module is loaded
if not init_openai():
    logger.error("Failed to initialize OpenAI API")

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
        if not client:
            logger.error("OpenAI client is not initialized!")
            return "Sorry, the AI service is not properly configured. Please contact the administrator."
            
        logger.info(f"Generating fun fact for coordinates: {latitude}, {longitude}")
        
        prompt = (
            "You are a knowledgeable local guide. "
            f"A person is at coordinates {latitude}, {longitude}. "
            "Share one interesting and lesser-known fact about a place, landmark, "
            "or historical event near these coordinates. "
            "Keep it concise (max 2-3 sentences) and engaging. "
            "Focus on unique, specific details rather than general information."
        )
        
        response = await client.chat.completions.create(
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
        
    except Exception as e:
        logger.error(f"Error generating fun fact: {str(e)}")
        if "auth" in str(e).lower() or "api key" in str(e).lower():
            return "There's an issue with the AI service authentication. Please check the API key configuration."
        return "I couldn't find an interesting fact about this location at the moment. Please try again later." 