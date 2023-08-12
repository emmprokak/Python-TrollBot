"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

from DataConfig import DataConfig
from RandomnessUtil import checkDeafenMuteTime

def validateCommandUser(username):
    return username in DataConfig.commandUsers

async def getChannelToJoin(bot):
    voiceChannels = []

    for server in bot.guilds:
        for channel in server.channels:
            if str(channel.type) == "voice":
                voiceChannels.append(channel)

    if len(voiceChannels) <= 0:
        raise Exception("ok, no voice channels, what the fuck for real now")

    targetVoiceChannel = voiceChannels[0]
    for channel in voiceChannels:
        if len(channel.members) > len(targetVoiceChannel.members):
            targetVoiceChannel = channel

    if len(targetVoiceChannel.members) <= 0:
        return None, False

    deafenMuteFun = checkDeafenMuteTime(targetVoiceChannel)

    return targetVoiceChannel, deafenMuteFun


def getSoundUrlByUserInput(action, localSound = False):
    if localSound:
        return f"{DataConfig.LOCAL_SOUND_DIR}{DataConfig.urlsByActionMapLocalFiles[action]}"
    else:
        return DataConfig.urlsByActionMap[action]


def isMalakaMessage(w):
    wLowerCase = w.lower()
    malakaWordList = ["malaka", "μαλάκα", "μαλακα"]
    return any([malakaWord in wLowerCase for malakaWord in malakaWordList])
