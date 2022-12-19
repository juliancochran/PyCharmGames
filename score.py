# simple object to represent a low score value for the game
# 12.16.2022
__author__ = 'Julian Cochran'

class Score:
    def __init__(self, inits, val):
        self.initials = inits
        self.points = val

    def __gt__(self, other):
        return self.points > other.points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.points == other.points

    def __str__(self):
        return self.initials + '\t' + str(self.points)