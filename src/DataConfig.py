"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

class DataConfig:
    EMPTY_STRING = ""
    SWEAR_REACTION = "swear"
    FAMILY_REFERENCE_REACTION = "family"
    VOICE_REACTION = "voice"

    LOCAL_SOUND_DIR = "localSounds/"

    commandUsers = [] # add your username here to be able to execute commands

    urlsByActionMap = { # fill dictionary with options for voice trolling
      "actionName" : "urlForYoutubeVideo"
    }

    urlsByActionMapLocalFiles = { # fill dictionary with options for voice trolling
        "localActionName" : "fileNameOfLocalSoundFile"
    }

    @staticmethod
    def getActionSoundEffectNameList():
        return list(DataConfig.urlsByActionMap.keys())

    @staticmethod
    def getCommonSwearWordList():
        return [ # fill list with swear words users might use
           "userSwearWord1"
        ]

    @staticmethod
    def getBotNoSwearingReplyList():
        return [ # fill list with bot replies to common swearwords
          "boyReply1"
        ]

    @staticmethod
    def getFamilySwearReplyList():
        return [ # fill list with reaction to common internet banter
            "Your father is pretty cool",
        ]
