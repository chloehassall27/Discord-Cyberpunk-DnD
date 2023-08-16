import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import threading
import dotenv
import lightbulb
import pymongo
from hikari import StartingEvent, StoppingEvent, Intents

from util.db import initDbHelper

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
                                            tlsAllowInvalidCertificates=True)
    bot.d.db = bot.d.mongoClient["originalServer"]
    bot.d.current_actions = bot.d.db["currentActions"]
    bot.d.players = bot.d.db["players"]
    bot.d.logs = bot.d.db["logs"]
    print(bot.d.mongoClient.server_info())
    initDbHelper(bot)
    bot.load_extensions_from("./plugins/", must_exist=True)


@bot.listen()
async def on_stopping(event: StoppingEvent) -> None:
    await bot.d.mongoClient.close()


def create_ping_server():
    port = 18000
    handler_object = SimpleHTTPRequestHandler
    my_server = socketserver.TCPServer(("", port), handler_object)

    print("serving at port:" + str(port))
    my_server.serve_forever()

# Run the bot
# Note that this is blocking meaning no code after this line will run
# until the bot is shut off
if __name__ == "__main__":
    threading.Thread(target=create_ping_server).start()
    bot.run()
