"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

from DataConfig import DataConfig
from LimitedPositionQueue import LimitedPositionQueue

class Context:
    nonExecutedTrollCount = 0
    initiateTroll = False

    botIsInVoiceChannel = False

    lastUsed = {
        DataConfig.SWEAR_REACTION: LimitedPositionQueue(),
        DataConfig.FAMILY_REFERENCE_REACTION: LimitedPositionQueue(),
        DataConfig.VOICE_REACTION: LimitedPositionQueue()
    }