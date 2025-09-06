def register(app, db):
    # register handlers
    @app.on_message(filters.command("mygame") & filters.group)
    async def mygame_handler(c, m):
        ...
