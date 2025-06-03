import os
from dotenv import load_dotenv

# Try to load .env file if it exists, but don't fail if it doesn't
try:
    load_dotenv()
except:
    pass

# Determine if we're in test mode
IS_TEST = os.getenv('TESTING', 'false').lower() == 'true'

# Bot settings
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
if not TELEGRAM_TOKEN and not IS_TEST:
    raise ValueError("TELEGRAM_TOKEN environment variable is not set")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
if not OPENAI_API_KEY and not IS_TEST:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Coordinates settings
COORDINATE_PRECISION = 4  # Number of decimal places for rounding coordinates 