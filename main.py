# imports
import discord
import asyncio
import wget

client = discord.Client()

TOKEN = ""

linkFound = False

@client.event
async def on_ready():
    print(f"logged in as {client.user.name}")
    print(f"with user ID: {client.user.id}")

def convertVmToTrue(message):
    rawUserMessage = str(message.content)
    videoLink = rawUserMessage.replace("vm.", "")
    return videoLink

def downloadLink(link):
    videoFile = wget.download(link, out="output.mp4")
    return

def checkForLink(message):
    userMessage = str(message.content)
    linkSearchCriteria = "vm.tiktok.com"

    if linkSearchCriteria in userMessage:
        print('link found')
        linkToDownload = convertVmToTrue(message)
    else:
        return


# logging
@client.event 
async def on_message(message):
    username = str(message.author).split('#')[0]
    userMessage = str(message.content)
    channelMessage = str(message.channel.name)
    print(f'User:{username}: Content:{userMessage} | In:{channelMessage}')

    if message.author == client.user:
        return
    checkForLink(message)

client.run(TOKEN)