import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from cmd import Bot
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
    #print(message)
    if message.content.startswith('.help'):
        await message.channel.send(bot.help())
    if message.content.startswith('.mge'):
        await message.channel.send(bot.bid(message))
    if message.content.startswith('.rank'):
        await message.channel.send(bot.statuss())
    await client.process_commands(message)
client.run(os.getenv('TOKEN'))