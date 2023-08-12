"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

import random as r
from RandomnessUtil import isYourLuckyDay, getNewReplyIdxExcludingPrevious, callBasedOnChance
from DataConfig import DataConfig
from Settings import Settings

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


def getUserMessageResponse(userMessage):
    if "your mom" in userMessage:
        return getFamilySwearReply()

    if any(word in userMessage for word in DataConfig.getCommonSwearWordList()):
        return callBasedOnChance(Settings.RESPOND_SWEAR_MESSAGE_PROBABILITY, getNoSwearingReply)