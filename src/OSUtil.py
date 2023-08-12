"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

import os, shutil

class OSUtilities:
    ytSoundsDir = "./ytSounds"
    maxAllowedDirSize = 1000000000

    @staticmethod
    def checkCleanupLocalSoundDir(dir = ytSoundsDir):
        totalDirSize = 0

        for path, dirs, files in os.walk(dir):
            for f in files:
                filepath = os.path.join(path, f)
                totalDirSize += os.path.getsize(filepath)

        if totalDirSize >= OSUtilities.maxAllowedDirSize:
            print("clearing yt folder...")
            OSUtilities.clearFolderContents(dir)

    @staticmethod
    def clearFolderContents(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        print("cleared yt folder")
