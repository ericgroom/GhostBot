import os
from discord.ext import commands
import aiohttp
import asyncio
import logging

import destiny

description = 'A bot for our Destiny 2 clan WGWD'

if 'DEV' in os.environ and os.environ['DEV'].lower() == 'true':
    from dev_utils import json_browser
else:
    def json_browser(*args): pass

keys = {
    'BUNGIE_KEY': os.environ['BUNGIE_KEY'],
    'BOT_TOKEN': os.environ['BOT_TOKEN'],
}

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='!', description=description)
session = aiohttp.ClientSession()
api = destiny.API(keys['BUNGIE_KEY'], session)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True, enabled=False, hidden=True)
async def test(ctx):
    """
    Counts the number of messages a user has sent in a channel
    """
    counter = 0
    tmp = await bot.say('Calculating messages...')
    async for log in bot.logs_from(ctx.message.channel, limit=100):
        if log.author == ctx.message.author:
            counter += 1

    await bot.edit_message(tmp, f'You have {counter} messages.')


@bot.command(enabled=False, hidden=True)
async def sleep():
    """
    Bots need naps too.
    """
    await asyncio.sleep(5)
    await bot.say('Done sleeping')


@bot.command()
async def playtime(account: str):
    """
    Shows how long a player has played D2 for across all characters.
    :param account: Battle.net account including tag
    """
    await bot.type()
    user = await api.get_user_from_battlenet(account)
    json_browser(user.json)
    await bot.say(f'{account} has played for {user.time_played}')


@bot.command()
async def light(account: str):
    """
    Shows a player's highest light on a character.
    :param account: Battle.net account including tag
    """
    await bot.type()
    user = await api.get_user_from_battlenet(account)
    await bot.say(f'{account}\'s highest light character has {user.highest_light} light')

@bot.command()
async def kda(account: str):
    """
    Shows a player's KDA in the crucible.
    :param account: Battle.net account including tag
    """
    await bot.type()
    user = await api.get_user_from_battlenet(account)
    await bot.say(f'{account}\'s PvP kda is {user.kda}')


@bot.command(hidden=True)
async def roast(account: str):
    """
    Shows how many times a user has committed suicide
    :param account: Battle.net account including tag
    """
    await bot.type()
    user = await api.get_user_from_battlenet(account)
    await bot.say(f'{account} has committed suicide {user.suicides} times')


if __name__ == "__main__":
    bot.run(keys['BOT_TOKEN'])
