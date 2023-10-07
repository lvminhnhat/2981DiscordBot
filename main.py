import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from cmd import Bot
from keep_alive import keep_alive
#config
load_dotenv()
intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.guilds = True
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)
bot = Bot()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    username  = str(message.author)
    userMessage = str(message.content)
    channel = str(message.channel)
    serverId = str(message.guild.id)
    serverName = str(message.guild.name)
    print( f"{username} said : '{userMessage}' form {channel}, server id: {serverId}, server name: {serverName}")
    # kiểm tra xem người chơi có chat trong đúng channel không?
    if channel != "mge-auction":
        return
    # kiểm tra xem người chơi có chat trong đúng server không?
    if serverId != "1054746385481736192":
        return
    #print(message)
    async with message.channel.typing():
        if message.content.startswith(('.h', '.help')):
            await message.reply(bot.help())
        elif message.content.startswith(('.m', '.mge')):
            await message.reply(bot.bid(message))
        elif message.content.startswith(('.r', '.rank')):
            await message.reply(bot.statuss())
        elif message.content.startswith(('.c', '.check')):
            await message.reply(bot.check_coins(message))
    await client.process_commands(message)
keep_alive()
client.run(os.getenv('TOKEN'))
