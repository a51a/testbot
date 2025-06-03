import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot settings
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is not set")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Coordinates settings
COORDINATE_PRECISION = 4  # Number of decimal places for rounding coordinates 