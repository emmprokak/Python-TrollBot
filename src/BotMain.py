"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

import asyncio
import discord as dis
from discord.ext import commands

import OSUtil
from SerializationStore import SerializationStore
from Settings import Settings
from TextGen import getUserMessageResponse, getFakeIPAddress, getRoleReply, getSongRequestResponse, getBotReplyResponse, \
    getMentionUserReply, getNicknameReply, getNicknameForUser
from YTDLSource import YTDLSource
from dotenv import load_dotenv
import os
from Context import Context
from helperFunctions import *
from RandUtil import getRandomActionName, isTimeForVoiceFun, isTimeForBotResponse, checkMentionSwearingUser, \
    timeForTargetedVoiceKick, timeForMixChannels, getRandomElementOfList

load_dotenv()
OPUS_PATH = os.getenv('OPUS_PATH')

def main():
    intents = dis.Intents.default()
    intents.members = True
    intents.messages = True
    intents.message_content = True
    bot = commands.Bot(description="Discord Bot", command_prefix=DataConfig.COMMAND_SYMBOL, intents=intents, help_command=None)
    dis.opus.load_opus(OPUS_PATH)

    if not dis.opus.is_loaded():
        print("Opus not loaded")
        exit(1)

    if not SerializationStore.localConfigExists():
        SerializationStore.storeSettings()
    else:
        SerializationStore.loadSettings()

    ### Bot Event Start ###

    @bot.event
    async def on_ready():
        print('logged in as {0.user}'.format(bot))

    @bot.event
    async def on_message(message):
        print(message.author.bot)
        messageText = message.content

        if message.author == bot.user:
            return

        await reactToMessage(message, messageText)

        if isinstance(messageText, str) and messageText[0] != DataConfig.COMMAND_SYMBOL:
            ctx = await bot.get_context(message)
            await checkDoCanonEvent(ctx, False)

        await bot.process_commands(message)

    @bot.event
    async def on_voice_state_update(member, before, after):
        if member == bot.user:
            return

        if member.voice is None or member.voice.channel is None or Context.botIsInVoiceChannel:
            Context.nonExecutedTrollCount += 1
            return

        if isCustomFeatureEnabled(DataConfig.CUSTOM_FEATURE_TARGETED_BULLYING) and\
                member.name == Context.targetedPersonName \
                and timeForTargetedVoiceKick() and member.voice.channel is not None:
            await asyncio.sleep(Settings.TARGET_BULLYING_VOICE_KICK_DELAY)
            await member.move_to(None)
            await asyncio.sleep(Settings.TARGET_BULLYING_VOICE_KICK_DELAY)

        if isCustomFeatureEnabled(DataConfig.CUSTOM_FEATURE_MIX_CHANNELS) and timeForMixChannels() and not Context.currentlyMixingChannels:
            print(f"calling check mix with " + str(member.guild.voice_channels))
            await checkMixMembersOnChannels(member.guild.voice_channels)
            return

        if isTimeForVoiceFun() and not Context.botIsInVoiceChannel and member.voice:
            Context.botIsInVoiceChannel = True
            await troll(None, getRandomActionName(), False, member.voice.channel)


    ### Bot Event End ###

    ### Bot Comm START ###

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

        await exitVoiceClientWhenSoundFinished(vc)
        Context.botIsInVoiceChannel = False
        OSUtil.OSUtilities.checkCleanupLocalSoundDir()

    """ Bot voice channel commands START """

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

    @bot.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    """ Bot voice channel commands END """

    """ Song Commands START """

    @bot.command(name='play_song', help='To play song')
    async def play(ctx, url):
        if not validateCommandUser(ctx.message.author.name):
            return

        await ctx.send(getSongRequestResponse())

        filename = await YTDLSource.from_url(url, loop=bot.loop)

        server = ctx.message.guild
        voiceClient = server.voice_client

        if not voiceClient:
            voiceChannel, deafenMuteIgnored = await getChannelToJoin(bot)
            voiceClient = await voiceChannel.connect()

        voiceClient.play(dis.FFmpegPCMAudio(executable="ffmpeg", source=filename))

        await exitVoiceClientWhenSoundFinished(voiceClient)

    @bot.command(name='ps', help='play song 2')
    async def playSong(ctx, url):
       await play(ctx, url)

    @bot.command(name='stop', help='Stops the song')
    async def stop(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    """ Song Commands END """

    """ Targeted Bullying Feature START """

    @bot.command(name='untarget', help='')
    async def targetPersonWrapper(ctx):
        previouslyTargetedPerson = Context.targetedPersonName

        if not previouslyTargetedPerson:
            return

        Context.targetedPersonName = DataConfig.EMPTY_STRING
        SerializationStore.storeSettings()
        await ctx.message.channel.send(f"{previouslyTargetedPerson} was untargeted successfully")

    @bot.command(name='target', help='')
    async def targetPersonWrapper(ctx, person):
        await targetPerson(ctx, person)


    @bot.command(name='trg', help='')
    async def targetPerson(ctx, person):
        if not validateCommandUser(ctx.message.author.name):
            return

        if not isCustomFeatureEnabled(DataConfig.CUSTOM_FEATURE_TARGETED_BULLYING):
            await sendFeatureNotEnabledMessage(DataConfig.CUSTOM_FEATURE_TARGETED_BULLYING)
            return

        targetFound = False
        Context.targetedPersonName = DataConfig.EMPTY_STRING
        for user in ctx.guild.members:
            if user.name == person:
                targetFound = True
                Context.targetedPersonName = person
                await user.move_to(None)

        SerializationStore.storeSettings()
        message = "Person was targeted successfully" if targetFound else "Person was not found in server"

        await ctx.message.channel.send(message)

    """ Targeted Bullying Feature END """

    """ Feature Management START """

    @bot.command(name='enable', help='')
    async def enableFeature(ctx, feature):
        if not validateCommandUser(ctx.message.author.name):
            return

        await requireFeatureInfo(ctx, feature)

    @bot.command(name='features', help='')
    async def displayFeatures(ctx):
        if not validateCommandUser(ctx.message.author.name):
            return

        message = "Custom features of bot instance:\n\n"
        count = 1
        for feature in DataConfig.customFeatureList:
            status = "ACTIVE" if Context.customFeatures[feature] else "INACTIVE"
            message += f"{count}. {feature}: {status}\n"
            count += 1

        await ctx.message.channel.send(message)

    @bot.command(name='disable', help='')
    async def disableFeature(ctx, feature):
        if not validateCommandUser(ctx.message.author.name):
            return

        if not customFeatureIsDefined(feature):
            return

        Context.customFeatures[feature] = False
        SerializationStore.storeSettings()
        await ctx.message.channel.send(f"Disabled feature {feature}")

    async def sendFeatureNotEnabledMessage(ctx, featureName):
        await ctx.message.channel.send(f"{featureName} not yet enabled. Please enable custom feature, before retrying command.")

    """ Feature Management END """

    @bot.command(name='members', help='')
    async def showMembers(ctx):
        await displayAllMembers(ctx)

    @bot.command(name='help', help='')
    async def showAvailableCommands(ctx):
        availForUsers = ", ".join(DataConfig.commandUsers)

        messageText = dis.Embed(title="Available Commands", description= "Available for user by: " + availForUsers, color=0x00ff00)

        for comm in DataConfig.helpCommands.keys():
            messageText.add_field(name=f"{DataConfig.COMMAND_SYMBOL}{comm}", value=DataConfig.helpCommands[comm], inline=False)

        await ctx.message.channel.send(embed=messageText)

    ### Bot Comm END ###

    ### HELPER

    async def checkMixMembersOnChannels(voiceChannels):
        if len(voiceChannels) <= 1:
            return

        Context.currentlyMixingChannels = True
        movedMembers = []

        for vc in voiceChannels:
            print(f"looping with vc = " + str(vc))
            for member in vc.members:
                print(f"\t member - " + str(member))
                if member not in movedMembers:
                    targetVoiceChannel = getRandomElementOfList(voiceChannels)
                    print(f"moving {member} to vc = {targetVoiceChannel}")
                    await member.edit(voice_channel= targetVoiceChannel)
                    movedMembers.append(member)


        Context.currentlyMixingChannels = False


    def customFeatureIsDefined(featureName):
        for feature in DataConfig.customFeatureList:
            if feature == featureName:
                return True

        return False

    async def displayAllMembers(ctx, showBots=False):
        for user in ctx.guild.members:
            if user == bot.user:
                continue

            message = "Server members:\n"
            count = 1

            for user in ctx.guild.members:
                if user == bot.user:
                    continue

                if user.bot and not showBots:
                    continue

                message += f"\n{count}. {user.name}"
                count += 1

        await ctx.message.channel.send(message)

    async def requireFeatureInfo(ctx, featureName):
        Context.currentEnablingFeature = featureName

        if not customFeatureIsDefined(featureName):
            return

        Context.customFeatures[featureName] = True
        SerializationStore.storeSettings()
        await ctx.message.channel.send(f"Feature '{featureName}' enabled successfully...")


    def logSwearingUser(username):
        if username in Context.peopleThatSwear:
            Context.peopleThatSwear[username] += 1
        else:
            Context.peopleThatSwear[username] = 1

    async def exitVoiceClientWhenSoundFinished(voiceClient):
        while voiceClient.is_playing():
            await asyncio.sleep(1)

        voiceClient.stop()
        await voiceClient.disconnect()

    async def reactToMessage(message, userMessageText):
        if isMalakaMessage(userMessageText):
            await message.add_reaction("🇬🇷")

        if message.author.bot and isTimeForBotResponse():
            await reactToBotMessage(message)
            return

        responseText = getUserMessageResponse(userMessageText, message.author)
        responseText = checkResponseForSpecialCase(message, responseText)

        mentionNicknameTrolled = await checkTrollSwearingUser(message, responseText)

        if responseText and not mentionNicknameTrolled:
            logSwearingUser(message.author.id)
            await message.reply(responseText)

    def checkResponseForSpecialCase(message, responseText):
        if responseText == "ip":
            return getFakeIPAddress()
        elif responseText == "role":
            role = getProperRole(message.author.roles)
            if role:
                return getRoleReply(role)

        return responseText # no special case, return input

    async def reactToBotMessage(message):
        responseText = getBotReplyResponse()
        if responseText:
            await message.reply(responseText)

    async def checkTrollSwearingUser(message, responseText):
        if responseText and message.author.id in Context.peopleThatGotMentioned:
            previousNickname = message.author.nick
            await message.author.edit(nick = getNicknameForUser())
            Context.peopleThatGotMentioned.remove(message.author.id)
            await message.channel.send(f"\'{previousNickname}\' <@{message.author.id}> {getNicknameReply()}")
            return True

        if responseText and checkMentionSwearingUser(*getMostSwearingUser()) and message.author.name != Context.targetedPersonName:
            Context.peopleThatSwear[message.author.id] = 0
            Context.peopleThatGotMentioned.append(message.author.id)
            await message.channel.send(f"<@{message.author.id}> {getMentionUserReply()}")
            return True

        return False

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