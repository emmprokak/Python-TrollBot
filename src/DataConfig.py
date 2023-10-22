"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

class DataConfig:
    EMPTY_STRING = ""
    SWEAR_REACTION = "swear"
    FAMILY_REFERENCE_REACTION = "family"
    VOICE_REACTION = "voice"
    ROLE_REACTION = "role"
    SONG_REQUEST_REACTION = "song"
    BOT_REACTION = "bot"
    MENTION_USER = "mention"
    NICKNAME_USER = "nickname"
    NICKNAMES_AVAILABLE = "actual_nicknames"

    LOCAL_SOUND_DIR = "localSounds/"

    CUSTOM_FEATURE_DEAFEN_MUTE = "deafen_mute"
    CUSTOM_FEATURE_TARGETED_BULLYING = "targeted_bullying"
    CUSTOM_FEATURE_MIX_CHANNELS = "mix_channels"

    customFeatureList = [CUSTOM_FEATURE_DEAFEN_MUTE, CUSTOM_FEATURE_TARGETED_BULLYING, CUSTOM_FEATURE_MIX_CHANNELS]

    commandUsers = [] # add your username here to be able to execute commands
    COMMAND_SYMBOL = "!"

    helpCommands = {
        "play_song [youtube link]": "Bot joins your channel and plays provided youtube video sound.",
        "ps [youtube link]" : "short version of play_song",
        "join" : "Bot joins your current voice channel and chills",
        "leave" : "Bot leaves voice channel",
        "members" : "Bot lists all server members",
        "features" : "Bot displays all custom features and respective status (ACTIVE/INACTIVE)",
        "enable [custom feature name]" : "Enables certain feature for bot",
        "disable [custom feature name]" : "Disables certain feature for bot",
        "target [username]" : "Bot targets user for targeted_bullying feature",
        "trg [username]" : "Short version of target",
        "untarget" : "User targeted by bot for targeted bullying is untargeted",
        "help" : "Get details for available commands"
    }

    urlsByActionMap = { # fill dictionary with options for voice trolling
        "actionName" : "urlForYoutubeVideo"
    }

    urlsByActionMapLocalFiles = { # fill dictionary with options for voice trolling
        "deafen_mute" : "fileNameOfLocalSoundFile.webm"
    }

    @staticmethod
    def getActionSoundEffectNameList():
        return list(DataConfig.urlsByActionMap.keys())

    @staticmethod
    def getCommonSwearWordList(): # fill list with swear words users might use
        return [
            "bad word 1"
        ]

    @staticmethod
    def getBotNoSwearingReplyList(): # fill list with bot replies to users swearing
        return [
            "ip",
            "role",
            "custom reply to swearing 1"
        ]

    @staticmethod
    def getFamilySwearReplyList(): # fill list with reaction to common internet banter
        return [
        "your father is pretty cool"
        ]

    @staticmethod
    def getRolesReplies(role): # fill list with bot reactions to user's role
        return [
          "role reply 1"
        ]

    @staticmethod
    def getSongRequestReplies(): # fill list with bot reactions to song requests
        return [
           "song request reply 1"
        ]

    @staticmethod
    def getBotReplies(): # fill list with bot reactions to other bot messages
        return [
         "reply to other bot 1"
        ]

    @staticmethod
    def getMentionUserReplies(): # fill list with bot replies when mentioning users
        return [
           "mention user reply 1"
        ]

    @staticmethod
    def getNicknameReplies(): # fill list with bot replies when changing a user's nickname
        return [
          "new nickname reply 1"
        ]

    @staticmethod
    def getActualNicknames(): # fill list with nicknames so that the bot will change user's nicknames
        return [
            "nickname1"
        ]

