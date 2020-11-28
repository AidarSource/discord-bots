# coding=utf8
from discord.ext import commands
from discord.ext import tasks
from discord import Embed
from algorithms.obslang_detect import check_slang
from algorithms.serverStatus import status, max_players
from data import get_data, get_exception, get_block, set_data, set_exception, set_block
from replics import media_replics, link_replics
import re
import json
import random

# prefix for bot commands
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}.')

    # this activates loop for renaming voice-channels
    voice_renamer.start()


# renames 4 voice-channels for actual gaming servers of discord server
@tasks.loop(minutes=5)
async def voice_renamer():
    # change web-links if you want to change to your server
    ze_server = 'https://www.gametracker.com/server_info/37.230.137.168:27015/'
    bhop_server = 'https://www.gametracker.com/server_info/37.230.137.168:27016/'
    arena_server = 'https://www.gametracker.com/server_info/37.230.137.168:27017/'
    public_server = 'https://www.gametracker.com/server_info/37.230.137.168:27018/'
    try:
        # getting voice-channel id of first server
        ze_channel = await bot.fetch_channel(739222175424184380)
        await ze_channel.edit(name=f'\U0001F4DC ZE: {status(ze_server)}/{max_players(ze_server)}')
        # getting voice-channel id of second server
        bhop = await bot.fetch_channel(739222222761230396)
        await bhop.edit(name=f'\U0001F4DC Bhop: {status(bhop_server)}/{max_players(bhop_server)}')
        # getting voice-channel id of third server
        arena = await bot.fetch_channel(739222247037730887)
        await arena.edit(name=f'\U0001F4DC Arena: {status(arena_server)}/{max_players(arena_server)}')
        # getting voice-channel id of fourth server
        public = await bot.fetch_channel(766412800561774592)
        await public.edit(name=f'\U0001F4DC Public: {status(public_server)}/{max_players(public_server)}')
    # shows a error when function get trouble in renaming voice-channels
    except Exception as e:
        print(e)


# blocks media files in specific text-channel
@bot.command()
@commands.has_permissions(administrator=True)
async def enable(ctx):
    channels = get_data()
    channels.append(ctx.channel.id)
    set_data(channels)
    await ctx.send('Restriction bot has been enabled for this text channel.')


# disables blocking media files in specific text-channel
@bot.command()
@commands.has_permissions(administrator=True)
async def disable(ctx):
    with open('channels.json', 'r') as data_file:
        data = json.load(data_file)
    for element in data:
        while True:
            try:
                data.remove(ctx.channel.id)
            except ValueError:
                break

    with open('channels.json', 'w') as data_file:
        data = json.dump(data, data_file)
    await ctx.send('Restriction bot has been disabled for this text channel.')


# enables algorithm to search obslang words in specific text-channel
@bot.command()
@commands.has_permissions(administrator=True)
async def obslang_enable(ctx):
    channels = get_block()
    channels.append(ctx.channel.id)
    set_block(channels)
    await ctx.send('Obscene Language filter has been enabled for this text channel.')

    with open('blocked.json', 'r') as JSON:
        json_blocked_dict = json.load(JSON)


# disables obslang in specific text-channel
@bot.command()
@commands.has_permissions(administrator=True)
async def obslang_disable(ctx):
    with open('blocked.json', 'r') as data_file:
        data = json.load(data_file)
    for element in data:
        while True:
            try:
                data.remove(ctx.channel.id)
            except ValueError:
                break

    with open('blocked.json', 'w') as data_file:
        data = json.dump(data, data_file)
    await ctx.send('Obscene Language filter has been disabled for this text channel.')

    with open('blocked.json', 'r') as JSON:
        json_blocked_dict = json.load(JSON)


# command for inserting exceptions to banned words by obslang command
@bot.command()
@commands.has_permissions(administrator=True)
async def systemcall_addexception(ctx):
    words = get_exception()
    words.append(ctx.message.content[25:])
    set_exception(words)
    
    await ctx.send('\U0001f5f3 Your word successfully added to exception list.')


# command for removal exception word
@bot.command()
@commands.has_permissions(administrator=True)
async def systemcall_delexception(ctx):
    with open('exception_words.json', 'r') as data_file:
        data = json.load(data_file)
    for element in data:
        while True:
            try:
                data.remove(ctx.message.content[25:])
            except ValueError:
                break

    with open('exception_words.json', 'w') as data_file:
        data = json.dump(data, data_file)

    await ctx.send('\U0001f5f3 Your word has been successfully removed from the list of exceptions.')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # this code is actually sucks, need to optimize. Opening json file for every message - bad idea
    with open('channels.json', 'r') as data_file:
        data = json.load(data_file)
    # this code is actually sucks, need to optimize.
    with open('blocked.json', 'r') as data_file:
        channels = json.load(data_file)
    # this code is actually sucks, need to optimize.
    with open('exception_words.json', 'r') as data_file:
        words = json.load(data_file)

    for text in channels:
        if text == message.channel.id:
            if message.author.guild_permissions.administrator:
                break

            for word in words:
                if message.content.lower() == word.lower():
                    return

            if check_slang(message.content):
                await message.delete()
                log = bot.get_channel(604351997646471218)
                await log.send(f'KGB Report \U0001f4f3 {message.author}: {message.content}')
                await message.author.send('Obscene language was detected, please do not use banned words in this channel \U0001f31d \nОбнаружена нецензурная лексика, искренне вас просим не использовать запрещенные слова \U0001f31d')

    for element in data:
        if element == message.channel.id:
            try:
                if re.search('https?://.*.(?:png|jpg|gif|jpeg)', message.content) or re.search('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', message.content) or re.search('(http(s|)://|)(www.|)(twitch|coub|imgur|prnt).(com|nl|tv|be|sc)', message.content):
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} {random.choice(link_replics)}")
                    media = bot.get_channel(521254726021677056)
                    await media.send(str(message.author) + ": " + str(message.content))
            except IndexError:
                break


    for element in data:
        if element == message.channel.id:
            try:
                if message.attachments[0].height:
                    await message.channel.send(f"{message.author.mention} {random.choice(media_replics)}")
                    media = bot.get_channel(521254726021677056)
                    embed = Embed(title=str(message.author) + ": ", description=str(message.content), color=0xff0000)
                    embed.set_image(url=message.attachments[0].url)
                    await media.send(embed=embed)
                    await message.delete()
                    break
            except IndexError:
                break

    await bot.process_commands(message)


# BOT TOKEN
bot.run('')