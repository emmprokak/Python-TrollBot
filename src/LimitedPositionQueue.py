"""
Created by MNS, Summer 2023
Dedicated to my friends with the intention of wreaking havoc in our discord servers.
"""

class LimitedPositionQueue:
    data = []
    keepLastUsedExpressionCount = 15

    def __init__(self, keepLastCount):
        if keepLastCount:
            self.keepLastUsedExpressionCount = keepLastCount

    def add(self, idx):
        if len(self.data) >= self.keepLastUsedExpressionCount:
            del self.data[0]
            self.data.append(idx)
        else:
            self.data.append(idx)

    def getData(self):
        return self.data

    def __str__(self):
        return f"Queue with data = {self.data}"