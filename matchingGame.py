# core class for ASCII art matching game in a 4x4 grid
# 12.16.2022
__author__ = 'Julian Cochran'

import random
import os
import time
from score import *


class MatchingGame:
    def __init__(self):
        self.board = [[' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]
        self.showboard = [['❑', '❑', '❑', '❑'], ['❑', '❑', '❑', '❑'], ['❑', '❑', '❑', '❑'], ['❑', '❑', '❑', '❑']]
        self.MATCHES = [[False, False, False, False], [False, False, False, False], [False, False, False, False],
                        [False, False, False, False]]
        self.symbols = ['&', '*', '$', '+', '%', '@', '^', '=']
        self.tries = 0

    def buildgrids(self):
        while len(self.symbols) > 0:
            item = self.symbols.pop(0)
            pair = 0
            while pair < 2:
                row = random.randrange(0, len(self.board))  # 3
                col = random.randrange(0, len(self.board[0]))  # 3
                if self.board[row][col] == ' ':
                    self.board[row][col] = item
                    pair += 1

    def printgrid(self, grid):
        for row in grid:
            #print(end='      ')
            for symbol in row:
                print(symbol, end=' ')
            print()

    def showGuess(self, move):
        self.showboard[move[0]][move[1]] = self.board[move[0]][move[1]]
        self.printgrid(self.showboard)

    def resetshowboard(self):
        for r in range(0, len(self.showboard)):
            for c in range(0, len(self.showboard[0])):
                if not self.MATCHES[r][c]:
                    self.showboard[r][c] = '❑'

    def addscore(self):
        filein = open('lowscores.txt', 'r')
        scores = []
        for line in filein:
            line = line.strip().split('\t')
            scores.append(Score(line[0], int(line[1])))
        filein.close()

        # max number of low scores is 10
        # format of a high score is INITIALS  SCORE
        # ex:
        # ABC 20
        # so the "highest" score, or most guesses, is in index -1 of scores
        # First, are there any high scores yet?
        if len(scores) < 10 or self.tries < scores[-1].score:
            initials = input('Congratulations! You earned a LOW score!\nPlease enter your initials: ').upper()
            if len(scores) < 10:
                scores.append(Score(initials, self.tries))
                scores.sort()
            else:
                scores[-1] = Score(initials, self.tries)
            fileout = open('lowscores.txt', 'w')
            for score in scores:
                fileout.write(str(score) + '\n')
            fileout.close()
        else:
            print('Sorry, you did not make it on the low scorers list.')
        # regardless of high score or not, close the file and print
        print('** Low scorers list **')

        for score in scores:
            print('     ', score.initials, '|', score.points)

    def run(self):
        self.tries = 0
        self.buildgrids()

        # play the game here
        while self.board != self.showboard:
            # each time the game loops, print the state of the board
            print('≈≈≈ BOARD STATUS ≈≈≈')
            self.printgrid(self.showboard)
            print()

            # get row col of the first move
            while True:
                try:
                    move1 = input('Enter row col for your first guess: ').split(' ')
                    move1[0] = int(move1[0])
                    move1[1] = int(move1[1])
                    if self.MATCHES[move1[0]][move1[1]]:
                        print('Space already uncovered, try again.')
                    else:
                        self.showGuess(move1)
                        break
                except Exception as e:
                    print('Invalid entry, try again', e)
            # get row col of the second move
            while True:
                try:
                    move2 = input('Enter row col for your second guess: ').split(' ')
                    move2[0] = int(move2[0])
                    move2[1] = int(move2[1])
                    if self.MATCHES[move2[0]][move2[1]]:
                        print('Space already uncovered, try again.')
                    elif move1 == move2:
                        print('Same location as your first move, try again.')
                    else:
                        self.showGuess(move2)
                        break
                except Exception as e:
                    print('Invalid entry, try again', e)

            # determine the symbols for each pick
            pick1 = self.board[move1[0]][move1[1]]
            pick2 = self.board[move2[0]][move2[1]]

            if pick1 == pick2:
                print('++ MATCH SELECTED ++')
                self.MATCHES[move1[0]][move1[1]] = True
                self.MATCHES[move2[0]][move2[1]] = True
            else:
                print('xx NOT A MATCH xx')
                self.resetshowboard()
            # input('hit return to continue')
            time.sleep(2)
            self.tries += 1
            os.system('clear')

        print('*** You won the game!! ***')
        self.printgrid(self.board)
        print('It took you', self.tries, 'tries to discover all matches on the board.')
        self.addscore()