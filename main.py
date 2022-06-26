# imports
import discord
import asyncio
import requests
import wget
import re
import os

client = discord.Client()

linkFound = False

TOKEN = "[DISCORD BOT TOKEN]"


@client.event
async def on_ready():
    print(f"logged in as {client.user.name}")
    print(f"with user ID: {client.user.id}")


def splitLink(url):
    return url.split('?')[0]

def removeOriginalFile(fileName):
    os.remove(fileName)
    return

def convertVmToTrue(message):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"}

    url = message
    response = requests.get(url, headers=headers)

    videoLink = response.url
    print(videoLink) # the correct url with the username
    return videoLink

def getVideoLink(link):
    url = "https://tiktok-info.p.rapidapi.com/dl/"
    querystring = {"link":link}
    headers = {
        "X-RapidAPI-Key": "MYAPIKEY",
        "X-RapidAPI-Host": "tiktok-info.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.text)
    print(url)
    url = (url[0])
    return url


def downloadLink(link):
    outputDirectory = "./tmp.mp4"
    wget.download(link, out=outputDirectory)
    return

def linkRequest(link):
    url = "https://tiktok-info.p.rapidapi.com/dl/"
    querystring = {"link":link}
    headers = {
        "X-RapidAPI-Key": "MYAPIKEY",
        "X-RapidAPI-Host": "tiktok-info.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)


def checkForLink(message):
    userMessage = str(message.content)
    linkSearchCriteria = "vm.tiktok.com"
    if linkSearchCriteria in userMessage.lower():
        return True
    else:
        return False

# logging
@client.event 
async def on_message(message):
    username = str(message.author).split('#')[0]
    userMessage = str(message.content)
    channelMessage = str(message.channel.name)
    print(f'User:{username}: Content:{userMessage} | In:{channelMessage}')

    if message.author == client.user:
        return

    # commands
    if userMessage.lower() == '!help':
        await message.channel.send(f"This is a help message for {username}")
        return

    linkFound = checkForLink(message)

    if linkFound == True:
        await message.channel.send(f"I found a TikTok link from {username}, let me download that for you!")
        # convert vm link to true link
        linkToDownload = convertVmToTrue(userMessage)
        # splits out the bit we don't need (after the '?')
        linkToDownload = splitLink(linkToDownload)
        # gets the .mp4 link via the api
        linkToDownload = getVideoLink(linkToDownload)
        # download the provided .mp4 link 
        downloadLink(linkToDownload)
        # upload video to channel
        await message.channel.send("Here is the original...")
        await message.channel.send(file=discord.File(r'tmp.mp4'))
        removeOriginalFile('tmp.mp4')
        return

client.run(TOKEN)
