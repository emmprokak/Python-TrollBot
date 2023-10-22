"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

import random as r
import datetime
from LimitedPositionQueue import LimitedPositionQueue
from Context import Context
from DataConfig import DataConfig
from Settings import Settings
# from helperFunctions import isCustomFeatureEnabled


def isYourLuckyDay(perc):
    num = r.randint(0, 100)
    return num <= perc

def getNewReplyIdxExcludingPrevious(list, typeOfReaction):
    maxRange = len(list) - 1
    idx = r.randint(0, maxRange)
    previousReplyIdxs = Context.lastUsed[typeOfReaction].getData()

    while len(previousReplyIdxs) > 0 and idx in previousReplyIdxs:
        idx = r.randint(0, maxRange)

    Context.lastUsed[typeOfReaction].add(idx)
    return idx


def getRandomActionName(localAction = False):
    if localAction:
        return r.choice(list(DataConfig.urlsByActionMapLocalFiles.keys()))
    else:
        actionList = DataConfig.getActionSoundEffectNameList()
        return actionList[getNewReplyIdxExcludingPrevious(actionList, DataConfig.VOICE_REACTION)]

def callBasedOnChance(perc, func):
    if isYourLuckyDay(perc):
        return func()
    else:
        return DataConfig.EMPTY_STRING

def isTimeForVoiceFun():
    # 28/07/2023 16:35:15
    dtString = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    time = dtString.split(" ")[1][0:-3]

    hour = int(time.split(":")[0])
    minutes = int(time.split(":")[1])

    if hour == minutes:
        return isYourLuckyDay(Settings.EARRAPE_MATCHING_TIME_PROBABILITY)

    multiplier = 1 + Context.nonExecutedTrollCount / 10
    Context.nonExecutedTrollCount = 0

    print(f"checking trolling probability")
    if 17 < hour < 21:
        return isYourLuckyDay(Settings.EARRAPE_AFTERNOON_PROBABILITY * multiplier)
    elif 21 < hour <= 23:
        return isYourLuckyDay(Settings.EARRAPE_EVENING_PROBABILITY * multiplier)
    elif 0 <= hour < 5:
        return isYourLuckyDay(Settings.EARRAPE_NIGHT_PROBABILITY * multiplier)
    else:
        return isYourLuckyDay(Settings.EARRAPE_MORNING_NOON_PROBABILITY * multiplier)

def checkDeafenMuteTime(voiceChannel):
    return len(voiceChannel.members) >= Settings.REQUIRED_MEMBERS_FOR_DEAFEN_MUTE and \
           isYourLuckyDay(Settings.DEAFEN_MUTE_PROBABILITY) and \
           Context.customFeatures[DataConfig.CUSTOM_FEATURE_DEAFEN_MUTE]

def isTimeForBotResponse():
    return isYourLuckyDay(Settings.RESPOND_TO_OTHER_BOT_PROBABILITY)

def checkMentionSwearingUser(username, timesSweared):
    print(f"check mention for {username}")
    return timesSweared is not None and timesSweared > 5 and \
           isYourLuckyDay(Settings.MENTION_SWEARING_USER_PROBABILITY)

def timeForTargetedVoiceKick():
    return isYourLuckyDay(Settings.TARGET_BULLYING_VOICE_KICK_PROBABILITY)

def timeForMixChannels():
    return isYourLuckyDay(Settings.MIX_CHANNELS_PROBABILITY)

def getRandomElementOfList(inputList):
    if not isinstance(inputList, list) or len(inputList) <= 0:
        return None

    return inputList[r.randint(0, len(inputList) - 1)]