# Raviv Haham, 208387951
# Peleg Haham, 208387969

import math
import pygame
import sys
import matplotlib.pyplot as plt
import numpy as np

# The screen pygame class
class PyGui:
    pygame.display.set_caption('SOM')
    # set isPause value to false so the game will run
    isPause = False
    # set the size of each cell to be 40
    cellSize = 40
    radius = 30
    backgroundColor = (255, 255, 255)

    # initialize the pygame screen board
    def __init__(self):
        self.numOfRows = 9
        self.numOfColumns = 5
        pygame.init()
        size = (self.width, self.height) = (self.numOfColumns * self.radius * 2) + 550, (self.numOfRows * self.radius) + 350
        self.screen = pygame.display.set_mode(size)


    # if the user press on the pause button we want to stop the genetic algorithm in this current iteration and set
    # isPause to true
    def stopFunc(self):
        while (self.isPause):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isPause = False

    # print the SOM screen and all the other information
    def printHexagonal(self, numOfIterations, bestScore, averageScore, worstScore, newDict, solutionNumber, avgDistancePerIterationArray, isFinished):
        # create a dictionary of all the colors
        colorsDict = {
            "colorEconomic1" : (255, 0, 0),
            "colorEconomic2" : (255, 51, 51),
            "colorEconomic3" : (255, 102, 102),
            "colorEconomic4" : (255, 153, 153),
            "colorEconomic5" : (255, 178, 102),
            "colorEconomic6" : (255, 204, 153),
            "colorEconomic7" : (255, 255, 153),
            "colorEconomic8" : (255, 255, 102),
            "colorEconomic9" : (204, 255, 153),
            "colorEconomic10" : (178, 255, 102)
        }


        # check if the user press on stop or quite
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.isPause = True
                    self.stopFunc()

        # set the background color screen
        self.screen.fill(self.backgroundColor)
        # set the font and the color of the text
        textFont = pygame.font.SysFont('comicsansms', 25)
        textColor = pygame.Color('blue')
        # create a txtSurface for each row and write the text
        txtSurface = textFont.render("Iteration: " + str(numOfIterations), True, textColor)
        self.screen.blit(txtSurface, (self.screen.get_height() / 2 , 5))
        if numOfIterations == 10:
            # create a txtSurface for each row and write the text
            textFont = pygame.font.SysFont('comicsansms', 22)
            textColor = pygame.Color('black')
            txtSurface = textFont.render("Press Enter To Continue", True, textColor)
            self.screen.blit(txtSurface, (self.screen.get_height() / 2 - 42, 55))

        # set the font and the color of the text
        textFont = pygame.font.SysFont('Helvetica', 20)
        textColor = pygame.Color('black')

        if isFinished:
            txtSurface = textFont.render("The Best Solution Number Is: " + str(solutionNumber), True, textColor)
            self.screen.blit(txtSurface, (15, 10))
        else:
            txtSurface = textFont.render("Solution Number: " + str(solutionNumber), True, textColor)
            self.screen.blit(txtSurface, (15, 10))
        txtSurface = textFont.render("Best Solution Distance: " + str(bestScore), True, textColor)
        self.screen.blit(txtSurface, (15, 30))
        txtSurface = textFont.render("Average Solution Distance: " + str(averageScore), True, textColor)
        self.screen.blit(txtSurface, (15, 50))
        txtSurface = textFont.render("Worst Solution Distance: " + str(worstScore), True, textColor)
        self.screen.blit(txtSurface, (15, 70))

        # draw all the board and set the color according to the results
        for i in range(self.numOfRows):
            # set the location of the number of each cell
            cellYLocation = i * (1.7 * self.radius) + 140
            if i <= 4:
                offset = -1 * 30 * i
                currentNumOfColumns = self.numOfColumns + i
            else:
                offset = 30 * i - 240
                currentNumOfColumns = self.numOfColumns - i + 8
            for j in range(currentNumOfColumns):
                cellXLocation = j * (2 * self.radius) + 265 + offset
                pygame.draw.polygon(self.screen, (20, 20, 20), [(cellXLocation + self.radius * math.sin(2 * math.pi * t / 6), cellYLocation + self.radius * math.cos(2 * math.pi * t / 6)) for t in range(6)], 3)
                currentTuple = (i, j)
                if currentTuple in newDict:
                    currentColor = "colorEconomic" + str(newDict[currentTuple])
                    pygame.draw.polygon(self.screen, colorsDict[currentColor], [(cellXLocation + (self.radius - 3) * math.sin(2 * math.pi * t / 6), cellYLocation + (self.radius - 3) * math.cos(2 * math.pi * t / 6)) for t in range(6)], 0)


        # -------------------------
        # print all the colors in the right side of the window
        txtSurface = textFont.render("Socioeconomic", True, textColor)
        self.screen.blit(txtSurface, (640, 15))
        txtSurface = textFont.render("status: ", True, textColor)
        self.screen.blit(txtSurface, (640, 35))
        txtSurface = textFont.render("1 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 37))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         50 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 0, 0), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 50 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)

        txtSurface = textFont.render("2 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 62))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         75 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 51, 51), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 75 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("3 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 87))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         100 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 102, 102), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 100 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("4 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 112))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         125 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 153, 153), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 125 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("5 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 137))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         150 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 178, 102), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 150 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("6 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 162))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         175 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 204, 153), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 175 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("7 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 188))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         200 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 255, 153), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 200 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("8 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 212))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         225 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (255, 255, 102), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 225 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("9 = ", True, textColor)
        self.screen.blit(txtSurface, (765, 237))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         250 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (204, 255, 153), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 250 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        txtSurface = textFont.render("10 = ", True, textColor)
        self.screen.blit(txtSurface, (757, 262))
        pygame.draw.polygon(self.screen, (20, 20, 20), [(805 + (self.radius - 21) * math.sin(2 * math.pi * t / 6),
                                                         275 + (self.radius - 21) * math.cos(2 * math.pi * t / 6))
                                                        for t in range(6)], 3)
        pygame.draw.polygon(self.screen, (178, 255, 102), [(805 + (self.radius - 23) * math.sin(
            2 * math.pi * t / 6), 275 + (self.radius - 23) * math.cos(2 * math.pi * t / 6)) for t in range(6)],
                            0)
        # -------------------------



        pygame.display.update()
        # if we finish to iterate over all the 10 SOM solutions we want to show the graph
        if isFinished:
            allIterations = np.arange(1, 10 + 1)
            plt.title("SOM 61 cells hexagon BOARD")
            plt.xlabel('Iteration Number')
            plt.ylabel('Average Distance')
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[0]), label="Solution 1")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[1]), label="Solution 2")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[2]), label="Solution 3")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[3]), label="Solution 4")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[4]), label="Solution 5")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[5]), label="Solution 6")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[6]), label="Solution 7")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[7]), label="Solution 8")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[8]), label="Solution 9")
            plt.plot(allIterations, np.array(avgDistancePerIterationArray[9]), label="Solution 10")
            plt.legend()
            plt.show()

        if solutionNumber == 11:
            self.isPause = True
            self.stopFunc()
