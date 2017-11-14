import discord
import aiohttp
import asyncio
import logging

import keys
import destiny

from dev_utils import json_browser

session = aiohttp.ClientSession()

api = destiny.API(keys.BUNGIE_KEY, session)

logging.basicConfig(level=logging.INFO)
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print(message)
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!time'):
        tokens = message.content.split()
        account = tokens[1]
        resp = await client.send_message(message.channel, f'Getting time played for {account}...')
        user = await api.get_user_from_battlenet(account)
        json_browser(user.json)
        await client.edit_message(resp, f'{account} has played for {user.time_played}')
    elif message.content.startswith('!light'):
        tokens = message.content.split()
        account = tokens[1]
        resp = await client.send_message(message.channel, f'Getting highest light for {account}...')
        user = await api.get_user_from_battlenet(account)
        await client.edit_message(resp, f'{account}\'s highest light character has {user.highest_light} light')
    elif message.content.startswith('!kda'):
        tokens = message.content.split()
        account = tokens[1]
        resp = await client.send_message(message.channel, f'Getting {account}\'s kda...')
        user = await api.get_user_from_battlenet(account)
        await client.edit_message(resp, f'{account}\'s PvP kda is {user.kda}')


client.run(keys.BOT_TOKEN)

