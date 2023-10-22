"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

from DataConfig import DataConfig
from RandUtil import checkDeafenMuteTime
from Context import Context

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
    malakaWordList = ["malaka", "μαλάκα", "μαλακα", "mlk", "μλκ"]
    return any([malakaWord in wLowerCase for malakaWord in malakaWordList])

def getProperRole(userRoles):
    for role in userRoles:
        if "everyone" not in role.name:
            return role

    return DataConfig.EMPTY_STRING

def getMostSwearingUser():
    return sorted(Context.peopleThatSwear.items(), key=lambda x: x[1], reverse=True)[0] \
        if len(Context.peopleThatSwear.items()) >= 1 else (None, None)

def isCustomFeatureEnabled(featureName):
    return Context.customFeatures[featureName]