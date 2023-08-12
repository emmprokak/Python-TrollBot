"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

import asyncio
import discord as dis
from discord.ext import commands

import OSUtil
from Settings import Settings
from TextGen import getUserMessageResponse, getFakeIPAddress
from YTDLSource import YTDLSource
from dotenv import load_dotenv
import os
from Context import Context
from helperFunctions import *
from RandomnessUtil import getRandomActionName, isTimeForVoiceFun

OPUS_PATH = "/opt/homebrew/Cellar/opus/1.3.1/lib/libopus.0.dylib"
load_dotenv()

def main():
    intents = dis.Intents.default()
    intents.members = True
    intents.messages = True
    intents.message_content = True
    bot = commands.Bot(description="Discord Bot", command_prefix="!", intents=intents)
    dis.opus.load_opus(OPUS_PATH)

    if not dis.opus.is_loaded():
        print("Opus not loaded")
        exit(1)

    ### Bot Event Start ###

    @bot.event
    async def on_ready():
        print('logged in as {0.user}'.format(bot))

    @bot.event
    async def on_message(message):
        print(f"received msg = {message}")
        messageText = message.content

        if message.author ==  bot.user:
            return

        await reactToMessage(message, messageText)

        if messageText[0] != "!":
            ctx = await bot.get_context(message)
            await checkDoCanonEvent(ctx, False)

        await bot.process_commands(message)

    @bot.event
    async def on_voice_state_update(member, before, after):
        # print(member.voice.channel)
        if member == bot.user:
            return

        if member.voice is None or member.voice.channel is None or Context.botIsInVoiceChannel:
            Context.nonExecutedTrollCount += 1
            return

        if isTimeForVoiceFun() and not Context.botIsInVoiceChannel:
            Context.botIsInVoiceChannel = True
            await troll(None, getRandomActionName(), False, member.voice.channel)


    ### Bot Event End ###

    ### Bot Comm START ###

    @bot.command(name='join', help='')
    async def join(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @bot.command(name='troll', help='')
    async def troll(ctx, action, checkUserAccess = True, voiceChannelToConnectTo = None, localSound = False):
        print("started troll")
        if checkUserAccess and not validateCommandUser(ctx.message.author.name):
            return

        vc = None
        channel = None
        deafenMuteFun = False
        useExistingVoiceClient = voiceChannelToConnectTo is not None
        filename = ""

        if localSound:
            filename = getSoundUrlByUserInput(getRandomActionName(True), True)
        else:
            filename = await YTDLSource.from_url(getSoundUrlByUserInput(action), loop=bot.loop)

        if useExistingVoiceClient:
            vc = await voiceChannelToConnectTo.connect()
        else:
            channel, deafenMuteFun = await getChannelToJoin(bot)
            if not channel:
                return

            vc = await channel.connect()

        if deafenMuteFun:
            await deafenAndMuteUsers(ctx, channel, vc, useExistingVoiceClient)
            return

        await playLocalSoundDirectlyToChannel(vc, filename)
        while vc.is_playing():
            await asyncio.sleep(1)

        vc.stop()
        await vc.disconnect()
        Context.botIsInVoiceChannel = False
        OSUtil.OSUtilities.checkCleanupLocalSoundDir()


    @bot.command(name='maybe_troll', help='')
    async def maybeTroll(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        await checkDoCanonEvent(ctx, False)


    @bot.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @bot.command(name='play_song', help='To play song')
    async def play(ctx, url):
        if not validateCommandUser(ctx.message.author.name):
            return

        try:
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(dis.FFmpegPCMAudio(executable="ffmpeg", source=filename))
            await ctx.send('**Now playing:** {}'.format(filename))
        except Exception as err:
            print("error = " + str(err))
            await ctx.send("The bot is not connected to a voice channel.")

    @bot.command(name='pause', help='This command pauses the song')
    async def pause(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @bot.command(name='resume', help='Resumes the song')
    async def resume(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @bot.command(name='stop', help='Stops the song')
    async def stop(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @bot.command(name='test', help='')
    async def test(ctx, type):
        if not validateCommandUser(ctx.message.author.name):
            return

        useLocalSoundEffect = True
        await troll(ctx, getRandomActionName(useLocalSoundEffect), True, localSound=useLocalSoundEffect)
        print("ended test")

    ### Bot Comm END ###

    ### HELPER

    async def reactToMessage(message, userMessageText):
        if isMalakaMessage(userMessageText):
            await message.add_reaction("🇬🇷")

        responseText = getUserMessageResponse(userMessageText)

        if responseText == "ip":
            await message.reply(getFakeIPAddress())
        elif responseText:
            await message.reply(responseText)

    async def playLocalSoundDirectlyToChannel(voiceClient, filename):
        voiceClient.play(dis.FFmpegPCMAudio(executable="ffmpeg", source=filename))

    async def checkDoCanonEvent(ctx, checkUser = True):
        if isTimeForVoiceFun():
            await troll(ctx, getRandomActionName(), checkUser)

    async def deafenAndMuteUsers(ctx, voiceChannel, voiceClient, useExistingVoiceClient):
        await playLocalSoundDirectlyToChannel(voiceClient, getSoundUrlByUserInput("deafen_mute", True))

        deafenPerson = False
        for person in voiceChannel.members:
            if person == bot.user:
                continue

            if deafenPerson:
                await person.edit(deafen=True)
            else:
                await person.edit(mute=True)

            deafenPerson = not deafenPerson

        await asyncio.sleep(Settings.DEAFEN_MUTE_SLEEP_TIME_SECONDS)

        # undo troll
        for person in voiceChannel.members:
            if person == bot.user:
                continue

            await person.edit(deafen=False)
            await person.edit(mute=False)

        voiceClient.stop()
        await voiceClient.disconnect()
        Context.botIsInVoiceChannel = False

    bot.run(os.getenv('AUTH_TOKEN'))

if __name__ == '__main__':
    main()