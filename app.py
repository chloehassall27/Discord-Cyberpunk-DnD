import os
import dotenv
import lightbulb
import pymongo
from hikari import StartingEvent, StoppingEvent, Intents
from util.db import initDbHelper
from util.config import config

dotenv.load_dotenv()
intents = (
    Intents.ALL_UNPRIVILEGED |
    Intents.GUILD_MEMBERS
)
# Instantiate a Bot instance
bot = lightbulb.BotApp(token=os.getenv('DISCORD_TOKEN'), intents=intents)


@bot.listen()
async def on_starting(event: StartingEvent) -> None:
    bot.d.mongoClient = pymongo.MongoClient(os.getenv('CUSTOMCONNSTR_DATABASE'),
                                            tls=True,
                                            tlsAllowInvalidCertificates=True,
                                            ConnectTimeoutMs=10000)
    bot.d.db = bot.d.mongoClient["originalServer"]
    bot.d.current_actions = bot.d.db["currentActions"]
    bot.d.players = bot.d.db["players"]
    bot.d.logs = bot.d.db["logs"]
    bot.d.config = config
    # print(bot.d.mongoClient.server_info())
    initDbHelper(bot)
    bot.load_extensions_from("./plugins/", must_exist=True)

@bot.command
@lightbulb.command("reload", "Reload the bot's plugins", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def reload(ctx: lightbulb.Context) -> None:
    for extension in bot.extensions:
        bot.reload_extensions(extension)
    ctx.respond("Cyberpunk DnD Bot reloaded")

@bot.listen()
async def on_stopping(event: StoppingEvent) -> None:
    bot.d.mongoClient.close()


# Run the bot
# Note that this is blocking meaning no code after this line will run
# until the bot is shut off
if __name__ == "__main__":
    bot.run()

