# import discord
# import os
# from dotenv import load_dotenv

# # Load the environment variables
# load_dotenv()

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def on_message(self, message):
#         # don't respond to ourselves
#         print(f"Receiveed message: {message.content}")
#         if message.author == self.user:
#             return

#         if message.content == 'ping':
#             await message.channel.send('pong')

# intents = discord.Intents.default()
# # intents.message_content = True
# client = MyClient(intents=intents)

# client.run(os.getenv('TOKEN'))

# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()a

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
    print(f"message: {message}")
    if message.content == "hello":
		# SENDS BACK A MESSAGE TO THE CHANNEL.
        await message.channel.send("hello man")

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(os.getenv('TOKEN'))
        
    