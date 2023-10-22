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
        DataConfig.SWEAR_REACTION: LimitedPositionQueue(15),
        DataConfig.FAMILY_REFERENCE_REACTION: LimitedPositionQueue(5),
        DataConfig.VOICE_REACTION: LimitedPositionQueue(15),
        DataConfig.ROLE_REACTION: LimitedPositionQueue(5),
        DataConfig.SONG_REQUEST_REACTION: LimitedPositionQueue(5),
        DataConfig.BOT_REACTION: LimitedPositionQueue(10),
        DataConfig.MENTION_USER: LimitedPositionQueue(5),
        DataConfig.NICKNAME_USER: LimitedPositionQueue(5),
        DataConfig.NICKNAMES_AVAILABLE: LimitedPositionQueue(5),
    }

    # filled on runtime
    peopleThatSwear = {

    }

    # filled on runtime
    peopleThatGotMentioned = []

    lynching = {

    }

    currentEnablingFeature = ""

    customFeatures = {
        DataConfig.CUSTOM_FEATURE_DEAFEN_MUTE : False,
        DataConfig.CUSTOM_FEATURE_TARGETED_BULLYING : False,
        DataConfig.CUSTOM_FEATURE_MIX_CHANNELS : False
    }

    targetedPersonName = ""
    currentlyMixingChannels = False # important to avoid recursive calls through voice state update calls

    customFeatureRequirementsMessages = {

    }

    customFeatureData = {
        DataConfig.CUSTOM_FEATURE_DEAFEN_MUTE : []
    }
