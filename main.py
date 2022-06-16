# Raviv Haham, 208387951
# Peleg Haham, 208387969


from random import randint, random
import random
import numpy as np
from gui import PyGui
import csv

# set global variable "numOfIterations" to true
numOfIterations = 0

class Node:
    # Constructor
    def __init__(self, vector, index, neighbors):
        self.vector = vector
        self.index = index
        self.neighbors = neighbors


# This function reads all the content from the csv file and create a matrix from that, and also return the max value
# of each column
def getMatrixData():
    cityNamesArray = []
    maxColVals = []
    maxColValsSize = 13
    for i in range(maxColValsSize):
        # initialize the "maxColVals" array with zeros
        maxColVals.append(0)

    # open the csv file to read it
    with open('Elec_24.csv', 'r') as csvfile:
        so = csv.reader(csvfile, delimiter=',', quotechar='"')
        economicClusterArray = []
        currentArray = []
        # we don't want the first line
        isFirstLine = True
        for row in so:
            if isFirstLine:
                isFirstLine = False
            else:
                economicClusterArray.append(int(row[1]))
                cityNamesArray.append(str(row[0]))

                totalVotes = int(row[2])
                # we want to use only the vote numbers per city
                tempArray = row[3:]
                # reversing the current kine using list slicing
                reverseTempArray = tempArray[::-1]
                # normalize the data by divide each vote number in the total votes number
                arrayAsInt = [int(x) for x in reverseTempArray]
                newArrayAsInt = [float(x) / float(totalVotes) for x in arrayAsInt]
                currentArray.append(newArrayAsInt)
                # update the "maxColVals" array to contain the max value of each column after each new row
                i = 0
                for value in newArrayAsInt:
                    if value >= maxColVals[i]:
                        maxColVals[i] = value
                    i += 1

        return currentArray, maxColVals, economicClusterArray, cityNamesArray




# This function calculates the neighbors of the current hexagon node according to it's (i,j) index
def getNeighbors(i, j, currentNumOfColumns):
    # We represent the hexagon as an array of arrays, so we will add the neighbors to the "currentNeighborsArray"
    # array according to the legality that created for this representation
    currentNeighborsArray = []
    if j > 0:
        currentNeighborsArray.append((i, j-1))
    if j < (currentNumOfColumns-1):
        currentNeighborsArray.append((i, j+1))
    if i > 0 and i <= 4 and j < (currentNumOfColumns-1):
        currentNeighborsArray.append((i-1, j))
    if i > 4 and i <= 8:
        currentNeighborsArray.append((i-1, j))
    if i <= 3:
        currentNeighborsArray.append((i + 1, j))
    if i >= 4 and i < 8 and j < (currentNumOfColumns-1):
        currentNeighborsArray.append((i+1, j))
    if i <= 3:
        if((i > 0) and  ( j > 0)):
            currentNeighborsArray.append((i-1, j-1))
        currentNeighborsArray.append((i+1, j+1))
    elif i == 4:
        if ((i > 0) and (j > 0)):
            currentNeighborsArray.append((i - 1, j - 1))
        if j > 0:
            currentNeighborsArray.append((i + 1, j - 1))
    else:
        currentNeighborsArray.append((i - 1, j + 1))
        if ((i < 8) and (j > 0)):
            currentNeighborsArray.append((i + 1, j - 1))
    return currentNeighborsArray




# This function find the closest hexagon node to the current centroid vector from all the hexagonal grid
def findClosestHexagonNode(currentCentroidVector, hexagon):
    minDistance = 9999999999
    ClosestHexagonNodeIndexArray = (None, None)
    numOfRows = 9
    numOfColumns = 5
    # run over all the nodes of the hexagon grid and find the index of the hexagon node that is the
    # closest to the current centroid vector
    for i in range(numOfRows):
        if i <= 4:
            currentNumOfColumns = numOfColumns + i
        else:
            currentNumOfColumns = numOfColumns - i + 8
        for j in range(currentNumOfColumns):
            currentNode = hexagon[i][j]
            hexagonNodeVector = currentNode.vector
            firstVec = np.array(currentCentroidVector)
            secondVec = np.array(hexagonNodeVector)
            # calculating Euclidean distance using linalg.norm()
            distance = np.linalg.norm(firstVec - secondVec)
            if distance < minDistance:
                minDistance = distance
                ClosestHexagonNodeIndex = (i, j)
    return ClosestHexagonNodeIndex, minDistance




# This function run over the hexagon grid and mapping the centroids to it's closest hexagon grid node (according to the
# vector of the hexagon grid node)
def vectorsMapping(hexagon, allCentroids):
    mappingArray = []
    centroidIndex = 0
    currentMinTotalDistance = 0
    # run over all the centroids vectors and create the mapping to all of them
    for currentVector in allCentroids:
        # find the index of the hexagon node that is the closest to the current centroid vector
        closestHexagonNodeIndex, currentMinlDistance = findClosestHexagonNode(currentVector, hexagon)
        currentMinTotalDistance += currentMinlDistance
        i = closestHexagonNodeIndex[0]
        j = closestHexagonNodeIndex[1]
        # add the mapping tuple to the "mappingArray" array
        mappingArray.append((centroidIndex, i, j))
        centroidIndex += 1

    return mappingArray, currentMinTotalDistance



# This function run over the hexagon with BFS algorithm and change the hexagonal grid according to the closest centroid
def bfs(visited, queue, hexagon, currentNode, closestCentroid):
    #learningRate = (100-numOfIterations)/100
    learningRate = 0.4
    percent = 0.3
    # add the first node to the visited list and to the queue
    visited.append(currentNode.index)
    queue.append((currentNode, percent))
    # run over all the nodes in the queue
    while queue:
        topQueue = queue.pop(0)
        topQueueNode = topQueue[0]
        currentPercent = topQueue[1]
        x = topQueueNode.index[0]
        y = topQueueNode.index[1]
        # update the vector of the node to be closer to the vector of the closest centroid
        realCurrentPercent = currentPercent * learningRate
        firstArray = np.array(topQueueNode.vector)
        npFirstArray = np.multiply(firstArray, (1-realCurrentPercent))
        secondArray = np.array(closestCentroid)
        npSecondArray = np.multiply(secondArray, realCurrentPercent)
        hexagon[x][y].vector = np.add(npFirstArray, npSecondArray)


        # add all the neighbours of the current node to the queue if they are not in the visited list yet
        for neighbour in topQueueNode.neighbors:
          if neighbour not in visited:
            neighbourNode = hexagon[neighbour[0]][neighbour[1]]
            # set the value of the "currentPercent" variable according to the level of the neighbour
            if currentPercent > 0.1:
                visited.append(neighbour)
                queue.append((neighbourNode, (currentPercent-0.1)))
            elif currentPercent == 0.1:
                visited.append(neighbour)
                queue.append((neighbourNode, (currentPercent-0.05)))
    # return the new hexagon with all the changes
    return hexagon



"""
# This function find the closest centroid to the current vector node from the hexagonal
def findClosestCentroid(currentNodeVector, allCentroids):
    minDistance = 9999999999
    centroidMinVector = []
    for currentCentroid in allCentroids:
        firstVec = np.array(currentNodeVector)
        secondVec = np.array(currentCentroid)
        # calculating Euclidean distance using linalg.norm()
        distance = np.linalg.norm(firstVec - secondVec)
        if distance < minDistance:
            minDistance = distance
            centroidMinVector = currentCentroid
    return centroidMinVector
"""



# This function creates one SOM iteration (updating the hexagonal for every node)
def doFullIteration(hexagon, allCentroids):
    # run over all the centroids vectors and map each one to it's close hexagon node call
    for currentVector in allCentroids:
        # find the index of the hexagon node that is the closest to the current centroid vector
        closestHexagonNodeIndex, minDistance = findClosestHexagonNode(currentVector, hexagon)
        i = closestHexagonNodeIndex[0]
        j = closestHexagonNodeIndex[1]
        currentNode = hexagon[i][j]
        closestCentroid = currentVector
        # List to keep track of visited nodes
        visited = []
        # Initialize a queue
        queue = []
        newHexagon = bfs(visited, queue, hexagon, currentNode, closestCentroid)
        hexagon = newHexagon
    return hexagon




# This function creates a new vector with 13 random values (between 0 to the max value that exists in each column)
def createNewVector(maxColVals):
    vectorSize = 13
    newVector = []
    for i in range(vectorSize):
        # random a float number between 0 to 1 and insert it to the new vector array
        newVector.append(random.uniform(0, maxColVals[i]))
        #newVector.append(random.uniform(0, 1))
    return newVector




# This function creates all the 61 nodes of the hexagon
def createHexagonGrid(maxColVals):
    numOfRows = 9
    numOfColumns = 5
    hexagon = []
    for i in range(numOfRows):
        hexagonRaw = []
        if i <= 4:
            currentNumOfColumns = numOfColumns + i
        else:
            currentNumOfColumns = numOfColumns - i + 8
        for j in range(currentNumOfColumns):
            # hexagonRaw.append(None)
            # create the random vector for the current hexagon node
            currentVector = createNewVector(maxColVals)
            # create the index for the current hexagon node
            currentIndex = (i, j)
            # save in array the index (as a tuple of i and j) of all the neighbors of the current hexagon node
            currentNeighbors = getNeighbors(i, j, currentNumOfColumns)

            currentNode = Node(currentVector, currentIndex, currentNeighbors)
            hexagonRaw.append(currentNode)
        hexagon.append(hexagonRaw)
    return hexagon


def main():
    global numOfIterations
    # we want to save the best solution all the time (the solution with the minimum total distance)
    minTotalDistance = 999999999999
    minTotalDistanceIndex = 0
    solutionDict = {}
    # we want to save the value of the solution with the max distance from all the iterations (the solution with the
    # max total distance)
    maxTotalDistance = -999999999999
    # we want to save the average value of all the solutions from all the iterations until now (the solution with the
    # max total distance)
    avergeDistance = -1
    allTotalDistance = []
    # create an array for the garph
    avgDistancePerIterationArray = []
    for i in range(10):
        avgDistancePerIterationArray.append([])
    # read all the content from the csv file and create a matrix from that
    allCentroids, maxColVals, economicClusterArray, cityNamesArray = getMatrixData()

    # we want to run the SOM algorithm 10 times and show the best solution at the end
    for i in range(10):
        # set the "noChangeFlag" flag to false
        noChangeFlag = False
        oldMappingArray = []
        numOfIterations = 0
        # create a full copy of "allCentroids" array
        randAllCentroids = allCentroids.copy()
        # create the hexagon (create all the 61 nodes of the hexagon with a random value in each vector for every node)
        hexagon = createHexagonGrid(maxColVals)
        # we want to run the SOM algorithm iteration as long has the mapping of the vectors to the hexagon grid doesn't
        # converge
        #while not noChangeFlag:
        while numOfIterations != 10:
            # increase the number of the iteration in one
            numOfIterations += 1
            # rand a new permutation to "randAllCentroids" array
            random.shuffle(randAllCentroids)
            # update the hexagonal grid according to all  the rules
            newHexagon = doFullIteration(hexagon, randAllCentroids)
            hexagon = newHexagon
            # mapping the centroids to their closest hexagon grid node (according to the vector of the hexagon grid node)
            mappingArray, currentMinTotalDistance = vectorsMapping(hexagon, allCentroids)
            # add the current average of all the distances to the array of the solutions
            avgDistancePerIterationArray[i].append(currentMinTotalDistance/len(allCentroids))
            # check if the current mapping is equals to the previous mapping
            identicalElements = set(mappingArray) & set(oldMappingArray)
            if len(identicalElements) == len(mappingArray):
                # set the "noChangeFlag" flag to true because there is no change in the mapping soo we want stop running
                # the SOM iteration
                noChangeFlag = True
            # else we want to keep running the SOM algorithm iteration and set the "oldMappingArray" array
            # to be the current "mappingArray" array
            else:
                oldMappingArray = mappingArray

            # convert the mappingArray to contain the economic of each city
            elementIndex = 0
            economicMappingArray = []
            for element in mappingArray:
                economicMappingArray.append((economicClusterArray[elementIndex], element[1], element[2]))
                elementIndex += 1
            # initialize a dictionary where the keys are all the cells of the hexagon that centroid vector mapped
            # to their cells, and the value is an empty array
            dict = {}
            for element in mappingArray:
                dict[(element[1], element[2])] = []

            for element in economicMappingArray:
                dict[(element[1], element[2])].append(element[0])
            newDict = {}
            for key in dict:
                npValuesArray = np.array(dict[key])
                newDict[key] = round(np.average(npValuesArray))

            # update the minimum total distance value
            if currentMinTotalDistance < minTotalDistance:
                minTotalDistance = currentMinTotalDistance
                solutionDict = newDict
                minTotalDistanceIndex = i

            # update the maximum total distance value
            if currentMinTotalDistance > maxTotalDistance:
                maxTotalDistance = currentMinTotalDistance

            allTotalDistance.append(currentMinTotalDistance)
            avergeDistance = np.sum(allTotalDistance) / len(allTotalDistance)

            SOPBoard = PyGui()
            SOPBoard.printHexagonal(numOfIterations, float(int(10000 * (minTotalDistance/len(allCentroids)))) / 10000, float(int(10000 * (avergeDistance/len(allCentroids)))) / 10000, float(int(10000 * (maxTotalDistance/len(allCentroids)))) / 10000, newDict, i+1,None, False)

        # print the cities list to the terminal
        print("* Solution Number " + str(i))
        cityIndex = 0
        for name in cityNamesArray:
            iName = str(mappingArray[cityIndex][1])
            jName = str(mappingArray[cityIndex][2])
            print("The city- " + name + " is represented by the cell (" + iName + "," + jName + ")" )
            cityIndex += 1
        print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        print()
        SOPBoard.isPause = True
        SOPBoard.stopFunc()

    # at the end of all the 10 iterations we want to show the best solution
    SOPBoard = PyGui()
    SOPBoard.printHexagonal(numOfIterations, float(int(10000 * (minTotalDistance/len(allCentroids)))) / 10000, float(int(10000 * (avergeDistance/len(allCentroids)))) / 10000, float(int(10000 * (maxTotalDistance/len(allCentroids)))) / 10000, solutionDict, minTotalDistanceIndex+1, avgDistancePerIterationArray, True)
    SOPBoard.isPause = True
    SOPBoard.stopFunc()

main()
