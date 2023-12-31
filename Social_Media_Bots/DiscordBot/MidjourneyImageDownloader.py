import asyncio
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
MIDJOURNEY_BOT_ID = os.getenv('MIDJOURNEY_BOT_ID')
# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance
bot = commands.Bot(command_prefix='$', intents=intents)

# # Specify the desktop directory as the save location
# image_location = "E:/Concept_Art_AI/Social_Media_Bots/Images"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Fetch the channel object
    channel = bot.get_channel(int(CHANNEL_ID))
    print(channel)

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return  # Don't respond to our own messages

#     if message.channel.id == int(CHANNEL_ID) and message.author.id == int(MIDJOURNEY_BOT_ID):
#         print('Reading message')

#         if message.attachments:  # Check if the message has attachments (media)
#             for attachment in message.attachments:
#                 # Build the complete file path to save on the location
#                 file_path = os.path.join(image_location, attachment.filename)

#                 if attachment.content_type.startswith('image'):
#                     # Download the attachment to the image directory
#                     await attachment.save(file_path)
#                     print(f'Downloaded: {file_path}')

@bot.command()
async def download_midjourney_images(ctx):
    home_directory = os.path.expanduser( '~' )
    path = os.path.join( home_directory, 'Documents', 'midjourney_images')
    if not os.path.exists(path):
        os.mkdir(path)
        print("Folder %s created!" % path)
    else:
        print("Folder %s already exists" % path)
    midjourney_messages = [message async for message in ctx.channel.history(limit=20) if message.author.id == int(MIDJOURNEY_BOT_ID)]
    for message in midjourney_messages:
        for attachment in message.attachments:
            # Build the complete file path to save on the location
            file_path = os.path.join(path, attachment.filename)
            if attachment.content_type.startswith('image'):
                # tasks.append(asyncio.create_task(attachment.read()))
                await attachment.save(file_path)
                print(f'Downloaded: {file_path}')
    
    # Send a message to the channel indicating that the images have been downloaded
    await ctx.send('The last 20 images generated by Midjourney have been downloaded in the Documents/midjourney_images folder.')

# Start the bot with your token
bot.run(BOT_TOKEN)