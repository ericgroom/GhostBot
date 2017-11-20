import discord
import aiohttp
import asyncio
import logging
from collections import namedtuple

import keys
import destiny

from dev_utils import json_browser

Command = namedtuple('Command', ['handler', 'active'])

logging.basicConfig(level=logging.INFO)
client = discord.Client()
session = aiohttp.ClientSession()
api = destiny.API(keys.BUNGIE_KEY, session)

commands = {}

def bot_command(cmd_str, active=True):
    def decorate(func):
        commands[cmd_str] = Command(func, active)
        return func
    return decorate

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print(message)
    tokens = message.content.split()
    if tokens[0] in commands.keys():
        command = commands[tokens[0]]
        if command.active:
            await command.handler(message)

@bot_command('!test')
async def test(message):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=100):
        if log.author == message.author:
            counter += 1

    await client.edit_message(tmp, 'You have {} messages.'.format(counter))

@bot_command('!sleep')
async def sleep(message):
    await asyncio.sleep(5)
    await client.send_message(message.channel, 'Done sleeping')

@bot_command('!time')
async def playtime(message):
    tokens = message.content.split()
    account = tokens[1]
    resp = await client.send_message(message.channel, f'Getting time played for {account}...')
    user = await api.get_user_from_battlenet(account)
    json_browser(user.json)
    await client.edit_message(resp, f'{account} has played for {user.time_played}')

@bot_command('!light')
async def highest_light(message):
    tokens = message.content.split()
    account = tokens[1]
    resp = await client.send_message(message.channel, f'Getting highest light for {account}...')
    user = await api.get_user_from_battlenet(account)
    await client.edit_message(resp, f'{account}\'s highest light character has {user.highest_light} light')

@bot_command('!kda')
async def kda(message):
    tokens = message.content.split()
    account = tokens[1]
    resp = await client.send_message(message.channel, f'Getting {account}\'s kda...')
    user = await api.get_user_from_battlenet(account)
    await client.edit_message(resp, f'{account}\'s PvP kda is {user.kda}')

@bot_command('!roast')
async def roast(message):
    tokens = message.content.split()
    account = tokens[1]
    resp = await client.send_message(message.channel, f'Generating sick burn...')
    user = await api.get_user_from_battlenet(account)
    await client.edit_message(resp, f'{account} has suicided {user.suicides} times')


if __name__ == "__main__":
    client.run(keys.BOT_TOKEN)
