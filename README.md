# New-gaming-bot

Telegram Pyrogram gaming bot scaffold with multiple mini-games.

## Quickstart
1. Copy `example_config.py` to `config.py` and set `API_ID`, `API_HASH`, `BOT_TOKEN`.
2. Create a virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

## Structure
- `games/` contains game modules. Each module must implement `register(app, db)`.
- `database.py` provides a simple JSON-backed store.
- `utils/` contains helpers.

## Antakshari
The Antakshari module supports creating a game in a group chat, players joining, and turn-based singing where each next word must start with the last letter of the previous.
