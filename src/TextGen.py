"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""


import random as r

from Context import Context
from RandUtil import isYourLuckyDay, getNewReplyIdxExcludingPrevious, callBasedOnChance
from DataConfig import DataConfig
from Settings import Settings
from helperFunctions import isCustomFeatureEnabled


def getFakeIPAddress():
    minRange = 0
    maxRange = 255
    num1 = r.randint(minRange, maxRange)
    num2 = r.randint(minRange, maxRange)
    num3 = r.randint(minRange, maxRange)
    num4 = r.randint(minRange, maxRange)

    return f"{num1}.{num2}.{num3}.{num4}"

def getNoSwearingReply():
    replies = DataConfig.getBotNoSwearingReplyList()
    return replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.SWEAR_REACTION)]


def getFamilySwearReply():
    replies = DataConfig.getFamilySwearReplyList()
    replyText = replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.FAMILY_REFERENCE_REACTION)]

    if isYourLuckyDay(Settings.RESPONSE_FAMILY_INSULT_ADDITION_PROBABILITY):
        replyText += " and you know it"

    return replyText


def getUserMessageResponse(userMessage, senderUser):
    if "your mom" in userMessage:
        return getFamilySwearReply()

    if isCustomFeatureEnabled(DataConfig.CUSTOM_FEATURE_TARGETED_BULLYING) and Context.targetedPersonName == senderUser.name:
        return callBasedOnChance(100, getNoSwearingReply)

    if any(word in userMessage for word in DataConfig.getCommonSwearWordList()):
        return callBasedOnChance(Settings.RESPOND_SWEAR_MESSAGE_PROBABILITY, getNoSwearingReply)


def getRoleReply(roleName):
    replies = DataConfig.getRolesReplies(roleName)
    return replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.ROLE_REACTION)]


def getSongRequestResponse():
    replies = DataConfig.getSongRequestReplies()
    return replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.SONG_REQUEST_REACTION)]

def getBotReplyResponse():
    replies = DataConfig.getBotReplies()
    return replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.BOT_REACTION)]

def getMentionUserReply():
    replies = DataConfig.getMentionUserReplies()
    return replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.MENTION_USER)]

def getNicknameReply():
    replies = DataConfig.getNicknameReplies()
    return replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.NICKNAME_USER)]

def getNicknameForUser():
    replies = DataConfig.getActualNicknames()
    return replies[getNewReplyIdxExcludingPrevious(replies, DataConfig.NICKNAMES_AVAILABLE)]
