# Fun Fact by Location Bot

A Telegram bot that provides interesting facts about locations when users share their coordinates. The bot uses OpenAI's GPT model to generate unique and engaging facts about places near the shared location.

## Features

- Accepts location sharing via Telegram
- Generates interesting facts about nearby places using OpenAI
- Provides real-time responses with loading states
- Handles errors gracefully

## Setup

1. Clone the repository:
```bash
git clone https://github.com/a51a/testbot.git
cd testbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your credentials:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

4. Run the bot:
```bash
python main.py
```

## Testing

Run the tests using:
```bash
python -m unittest discover tests
```

## Deployment

The bot is configured for deployment on Railway. To deploy:

1. Create a new project on [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Add the following environment variables in Railway:
   - `TELEGRAM_TOKEN`
   - `OPENAI_API_KEY`
4. Deploy the project

## Usage

1. Start a chat with your bot on Telegram
2. Share your location
3. Receive an interesting fact about a nearby place or landmark

## Development

- Written in Python using aiogram framework
- Uses OpenAI's GPT-4.1-mini model for fact generation
- Implements proper error handling and logging
- Follows PEP 8 style guide (use `black` for formatting)

## License

MIT 