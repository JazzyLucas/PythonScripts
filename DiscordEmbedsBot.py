import os
import re
import discord
import requests
import tweepy
import configparser
from bs4 import BeautifulSoup

### Config
config = configparser.ConfigParser(interpolation=None)
config.read('config.txt')
DISCORD_TOKEN = config['DISCORD']['DISCORD_TOKEN']
TWITTER_API_KEY = config['TWITTER']['TWITTER_API_KEY']
TWITTER_API_SECRET = config['TWITTER']['TWITTER_API_SECRET']
TWITTER_BEARER_TOKEN = config['TWITTER']['TWITTER_BEARER_TOKEN']
INSTAGRAM_APP_SECRET = config['INSTAGRAM']['INSTAGRAM_APP_SECRET']

### Inits
# Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    
    #iFunny
    if 'ifunny.co/' in message.content:
        send_message = ":slight_smile: iFunny link from: " + message.author.mention + " :slight_smile:"

        # Extract the link from the message
        url = None
        words = message.content.split()
        for word in words:
            if word.startswith('https://ifunny.co/'):
                url = word
                break

        if url:
            # Send a request to the URL and retrieve the HTML
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers)
            html = response.text
            send_message += "\nOriginal Link: <" + url + ">"

            # Parse the HTML and extract the video link
            soup = BeautifulSoup(html, 'html.parser')
            video_element = soup.find('video')
            print(video_element)
            if video_element and 'data-src' in video_element.attrs:
                video_link = video_element['data-src']
                send_message += "\nVideo Link: " + video_link + ""

            await message.channel.send(send_message)
            await message.delete()

    # Twitter
    if 'twitter.com/' in message.content:
        send_message = ":bird: Twitter link from: " + message.author.mention + " :bird:"

        # Extract the link  from the message
        url = None
        words = message.content.split()
        for word in words:
            if word.startswith('https://twitter.com/'):
                url = word
                break

        if url:
            # Authenticate with the Twitter API
            auth = tweepy.OAuth2BearerHandler(TWITTER_BEARER_TOKEN)
            api = tweepy.API(auth)
            send_message += "\nOriginal Link: <" + url + ">"

            # Get the tweet
            try:
                match = re.search(r"status/(\d+)", url)
                if match:
                    url = match.group(1)
                # Check if the tweet has a video attachment
                tweet = api.get_status(url, tweet_mode='extended')
                media_entities = tweet.extended_entities.get('media', [])
                for media in media_entities:
                    # Check if the media entity is a video
                    if 'video_info' in media:
                        video_link = media['video_info']['variants'][0]['url']
                        send_message += "\nVideo Link: " + video_link + ""
            except tweepy.errors.NotFound:
                send_message += "404 Tweet not found."

            await message.channel.send(send_message)
            await message.delete()

    # Instagram
    if 'instagram.com/' in message.content:

        # Extract the link  from the message
        url = None
        words = message.content.split()
        for word in words:
            if word.startswith('https://twitter.com/'):
                url = word
                break

        if url:
            print("TODO: Instagram")
            # Authenticate with the Instagram API
            # TODO
            # Get the tweet
            # TODO

client.run(DISCORD_TOKEN)
