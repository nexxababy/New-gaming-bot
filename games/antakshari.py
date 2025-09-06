from pyrogram import filters
from pyrogram.types import Message
from main_utils import normalize
from utils import validators

GAMES = {}

class AntakshariGame:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.players = []
        self.current_index = 0
        self.started = False
        self.last_word = None
        self.scores = {}

    def add_player(self, user_id, name):
        if user_id in [p[0] for p in self.players]:
            return False
        self.players.append((user_id, name))
        self.scores[str(user_id)] = 0
        return True

    def start(self):
        if len(self.players) < 2:
            return False
        self.started = True
        self.current_index = 0
        return True

    def current_player(self):
        if not self.players:
            return None
        return self.players[self.current_index]

    def advance(self):
        self.current_index = (self.current_index + 1) % len(self.players)


async def antakshari_start(client, message: Message):
    chat_id = message.chat.id
    GAMES.setdefault(chat_id, AntakshariGame(chat_id))
    game = GAMES[chat_id]
    if game.started:
        await message.reply_text("Game already started in this chat.")
        return
    game.add_player(message.from_user.id, message.from_user.first_name)
    game.start()
    await message.reply_text(f"Antakshari started! Players: {', '.join([p[1] for p in game.players])}\n{game.current_player()[1]}'s turn. Send a word to begin.")


async def antakshari_join(client, message: Message):
    chat_id = message.chat.id
    GAMES.setdefault(chat_id, AntakshariGame(chat_id))
    game = GAMES[chat_id]
    added = game.add_player(message.from_user.id, message.from_user.first_name)
    if not added:
        await message.reply_text("You're already in the game.")
    else:
        await message.reply_text(f"{message.from_user.first_name} joined the Antakshari game.")


async def antakshari_word(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in GAMES:
        return
    game = GAMES[chat_id]
    if not game.started:
        return
    user = message.from_user
    current = game.current_player()
    if current[0] != user.id:
        return
    word = message.text.strip()
    if game.last_word is None:
        game.last_word = word
        await message.reply_text(f"Accepted: {word}. Next should start with '{normalize(word)[-1]}'\nNext: {game.players[(game.current_index+1)%len(game.players)][1]}")
        game.advance()
        return
    if validators.valid_start(game.last_word, word):
        game.last_word = word
        game.scores[str(user.id)] += 1
        await message.reply_text(f"Good! {user.first_name} gets a point. Current score: {game.scores}")
        game.advance()
    else:
        game.scores[str(user.id)] = max(0, game.scores.get(str(user.id),0)-1)
        await message.reply_text(f"Invalid start. {user.first_name} loses a point. Current score: {game.scores}")
        game.advance()


def register(app, db):
    app.add_handler(filters.command("antakshari_start") & filters.group, antakshari_start)
    app.add_handler(filters.command("antakshari_join") & filters.group, antakshari_join)
    app.add_handler(filters.text & filters.group, antakshari_word)
