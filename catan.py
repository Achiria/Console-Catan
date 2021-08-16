#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import print_function
from collections import deque
from os import system, name
import math
import sys
import time
import random

class bcolors:
    PLAYERBLUE = '\033[1;94m'
    PLAYERRED = '\033[1;91m'
    PLAYERYELLOW = '\033[1;93m'
    PLAYERGREEN = '\033[1;92m'
    PLAYERPURPLE = '\033[1;95m'

    # SHEEP = 
    # HAY = 
    # WOOD = 
    # BRICK = 
    # ORE = 

    WATER = '\033[34m'
    WATERSOLID = '\033[34m\033[0;104m'
    
    OKBLUE = '\033[34m'
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class commands:
    start = ['start', 'load', 'exit']
    creatingGame = ['exit']
    choosingColor = ['blue', 'green', 'red', 'yellow', 'purple', 'exit']
    beforeTurn = ['roll', 'play']
    inTurn = ['build', 'trade', 'dev']

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ord(ch) == 3 or ord(ch) == 26:
            sys.exit()
        return ch

class coord(object):
    # initialize the coordinate object
    #
    # @param x         the x coordinate
    # @param y         the y coordinate
    # @param water     0 if coordinate is on land, 1 if in water
    # @param pointType 0 if none, 1 if road up type, 2 if road flat type, 3 if road down type, 4 if building type, 5 if resource type
    # @param building  0 if no building, 1 if road or settlement, 2 if city
    # @param owner     the ID of the player who owns the building if any
    def __init__(self, x, y, water, pointType, resource="", number=0, building=0, owner=None):
        self.x = x
        self.y = y
        self.water = water
        self.pointType = pointType
        self.building = building
        self.owner = owner
        self.active = 0
        self.resource = resource
        self.number = number

    # overwrite the print function
    #
    # @return will return the coordinate in format (x, y)
    def __str__(self):
        return "(" + str(self.y) + ", " + str(self.x) + ") water: " + str(self.water) + " pointType: " + str(self.pointType) + " building: " + str(self.building)

# class tilePart(object):
#     def __init__(self, x, y, ownedCoords=[]):
#         self.x = x
#         self.y = y
#         self.ownedCoords = ownedCoords
        
# class tileWhole():
#     def __init__(self, topTile, bottomTile, resource, shutdown=0):
#         self.topTile = topTile
#         self.bottomTile = bottomTile
#         self.resource = resource
#         self.shutdown = shutdown

class pointGrid():
    def __init__(self, size):
        self.size = size
        width = size
        height = int(math.floor(width/2.0))    #14
        middle = int(math.floor(height/2.0))   #7
        pointTypePattern = deque([3, 4, 2, 4, 1, 0, 5, 0])
        numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        resources = ["s", "s", "s", "s", "h", "h", "h", "h", "w", "w", "w", "w", "b", "b", "b", "o", "o", "o"]

        points = []
        for y in range(height+1):
            pointTypePattern.rotate(4)
            points.append([])
            for x in range(width):
                water = 0
                pointType = pointTypePattern[x%8]   
                number = 0
                resource = ""

                #attempting to create board programmatically...

                # 0 and 1 always all water
                if (y == 0 or y == 1 or y == height-1 or y == height):
                    water = 1
                elif (y < middle - 2):
                    # print (height - 1)- (4*(y - 2) + 1)
                    if (x < (height) - (4*(y - 2) + 1)):
                        water = 1
                    elif (x > (height) + (4*(y - 2) + 1)):
                        water = 1
                elif (y > middle + 2):
                    if (x < (height) - (4*abs((y - (middle + 5))) + 2)):
                        water = 1
                    elif (x > (height) + (4*abs((y - (middle + 5))) + 2)):
                        water = 1
                else:
                    if (x < 4 or x > 24):
                        water = 1

                # Assign resource and number
                if pointType == 5 and water == 0:
                    # TODO randomize arrays before popping
                    number = numbers.pop()
                    if number == 7:
                        resource = ""
                    else: 
                        resource = resources.pop()
                    
                point = coord(x, y, water, pointType, resource, number)
                points[y].append(point)
        self.width = width
        self.height = height
        self.points = points

    def __str__(self):
        height = self.height
        width = self.width
        points = self.points

        toReturn = ""

        for y in range(height+1):
            if (y != 0):
                toReturn += "\n"
            for x in range(width):
                if (points[y][x].water == 1):
                    color = bcolors.WATER
                else:
                    color = bcolors.ENDC
                
                # if highlighted
                if (points[y][x].active == 1):
                    color = bcolors.HEADER
                    toPrint = chr(9608).encode('utf-8')
                # if empty
                elif (points[y][x].pointType == 0):
                    # print empty or first numeral of large number
                    toPrint = " "
                    if points[y][x+1].pointType == 5 and points[y][x+1].number > 9:
                        toPrint = "1"
                # if resource type
                elif (points[y][x].pointType == 5):
                    if points[y][x].water == 1:
                        toPrint = " "
                    else:
                        # print second numeral
                        if points[y][x].number > 9:
                            toPrint = str(points[y][x].number - 10)
                        else:
                            toPrint = str(points[y][x].number)
                # if building or any road type
                else:
                    # if any building present get owner color
                    if points[y][x].building != 0:
                        ownerColor = points[y][x].owner.color
                        if ownerColor == "red":
                            color = bcolors.PLAYERRED
                        elif ownerColor == "blue":
                            color = bcolors.PLAYERBLUE
                        elif ownerColor == "green":
                            color = bcolors.PLAYERGREEN
                        elif ownerColor == "yellow":
                            color = bcolors.PLAYERYELLOW
                        elif ownerColor == "purple":
                            color = bcolors.PLAYERPURPLE
                    # if road up type
                    if (points[y][x].pointType == 1):
                        toPrint = "/"
                    # if road flat type
                    elif (points[y][x].pointType == 2):
                        toPrint = "_"
                    # if road down type
                    elif (points[y][x].pointType == 3):
                        toPrint = "\\"
                    # if building type
                    elif (points[y][x].pointType == 4):
                        # if no building
                        if (points[y][x].building == 0):
                            toPrint = "_"
                        # if settlement
                        elif (points[y][x].building == 1):                            
                            # toPrint = chr(5169).encode('utf-8') + bcolors.ENDC.encode('utf-8') + chr(818).encode('utf-8')
                            toPrint = "π".encode('utf-8') + bcolors.ENDC.encode('utf-8') + chr(818).encode('utf-8')
                        # if city
                        elif (points[y][x].building == 2):
                            # toPrint = chr(5169).encode('utf-8') + chr(831).encode('utf-8') + bcolors.ENDC + chr(818).encode('utf-8')
                            toPrint = "∆".encode('utf-8') + bcolors.ENDC + chr(818).encode('utf-8')
                try:
                    toAdd = color + toPrint.decode('utf-8') + bcolors.ENDC
                except (UnicodeDecodeError, AttributeError):
                    toAdd = color + toPrint + bcolors.ENDC
                toReturn += toAdd
        return toReturn

    def getPoint(self, x, y):
        return self.points[y][x]

    def moveCursor(self, currentPosition, direction):
        print(self.height)
        print(currentPosition.y)
        currentPosition.active = 0
        if direction == 'up':
            currentPosition = self.points[currentPosition.y-1][currentPosition.x]
        if direction == 'down':
            if currentPosition.y == self.height - 1:
                currentPosition = self.points[0][currentPosition.x]
            else:
                currentPosition = self.points[currentPosition.y+1][currentPosition.x]
        if direction == 'left':
            currentPosition = self.points[currentPosition.y][currentPosition.x-1]
        if direction == 'right':
            currentPosition = self.points[currentPosition.y][currentPosition.x+1]
        currentPosition.active = 1
        return currentPosition

class board():
    def __init__(self, points):
        print("")
            
class player():
    def __init__(self, number, name, color):
        self.number = number
        self.name = name
        self.color = color
        self.cards = {'hay': 0, 'sheep': 0, 'wood': 0, 'brick': 0, 'ore': 0}
        self.points = 0
        self.settlementCount = 5
        self.cityCount = 4
        self.roadCount = 15
        self.devCards = {'knight': 0, 'roadBuilder': 0, 'yearOfPlenty': 0, 'monopoly': 0, 'victoryPoint': 0}
        self.settlements = []
        self.cities = []
        self.roads = []
    
    def __str__(self):
        toReturn = ""
        return toReturn
    
    def getCards(self):
        return ('hay: ' + str(self.cards['hay']) + ', sheep: ' + str(self.cards['sheep']) + ', wood: ' + str(self.cards['wood']) + ', brick: ' + str(self.cards['brick']) + ', ore: ' + str(self.cards['ore']))

    def getDevCards(self):
        toReturn = ""
        if player.devCards.get('knight') > 0:
            toReturn += "knight: " + player.devCards.get('knight')
        if player.devCards.get('roadBuilder') > 0:
            if len(toReturn) > 0:
                toReturn += ", "
            toReturn += "road builder: " + player.devCards.get('roadBuilder')
        if player.devCards.get('yearOfPlenty') > 0:
            if len(toReturn) > 0:
                toReturn += ", "
            toReturn += "year of plenty: " + player.devCards.get('yearOfPlenty')
        if player.devCards.get('monopoly') > 0:
            if len(toReturn) > 0:
                toReturn += ", "
            toReturn += "monopoly: " + player.devCards.get('monopoly')
        if player.devCards.get('victoryPoint') > 0:
            if len(toReturn) > 0:
                toReturn += ", "
            toReturn += "victory Point: " + player.devCards.get('victoryPoint')
        if len(toReturn) > 0:
            return toReturn
        else:
            return "none"

def checkCommand(command):
    commandStack.append(command)
    if (command == "help"):
        commandStack.pop()
        print("Available commands: ", end="")
        for item in iter(availableCommands):
            print(item + " ", end="")
        print("")
        # time.sleep(1.5)
        command = input("Enter one of the available commands: ")
        checkCommand(command)
    elif (command == "exit"):
        if inGame:
            command = input("Any unsaved progress will be lost; are you sure you want to quit? y/n: ")
            valid = 0
            while valid == 0:
                if command == "y":
                    exit()
                elif command == "n":
                    print("Your game probably just broke. Sorry.")
                    return 0
                else:
                    command = input("Please enter y or n: ")
        else:
            exit()
    else:
        validCommand = 0
        for item in iter(availableCommands):
            if (command == item):
                validCommand = 1
                break
        if validCommand == 0:
            commandStack.pop()
            newCommand = input("Command not available. Type help to see available commands or enter valid command: ")
            checkCommand(newCommand)
        else:
            return 1

def checkCards(command, player):
    if command == "road":
        if player.cards.get('wood') > 1 and player.cards.get('brick'):
            return 1
    elif command == "settlement":
        if player.cards.get('hay') > 1 and player.cards.get('sheep') > 1 and player.cards.get('wood') > 1 and player.cards.get('brick') > 1:
            return 1
    elif command == "city":
        if player.cards.get('hay') > 2 and player.cards.get('ore') > 3:
            return 1
    elif command == "devCard":
        if player.cards.get('hay') > 1 and player.cards.get('sheep') > 1 and player.cards.get('ore') > 1:
            return 1
    return 0
    
def getResources(coord, points, roll=0):
    resources = []
    # left side
    if points.getPoint(coord.x+1, coord.y).pointType == 2:
        resource = points.getPoint(coord.x+1, coord.y+1).resource
        if resource != "":
            resources.append(resource)
        resource = points.getPoint(coord.x+1, coord.y-1).resource
        if resource != "":
            resources.append(resource)
        resource = points.getPoint(coord.x-3, coord.y).resource
        if resource != "":
            resources.append(resource)
    # right side
    if points.getPoint(coord.x+1, coord.y).pointType == 1:
        resource = points.getPoint(coord.x+2, coord.y).resource
        if resource != "":
            resources.append(resource)
        resource = points.getPoint(coord.x-1, coord.y-1).resource
        if resource != "":
            resources.append(resource)
        resource = points.getPoint(coord.x-1, coord.y+1).resource
        if resource != "":
            resources.append(resource)
    
    toReturn = {'hay': 0, 'sheep': 0, 'wood': 0, 'brick': 0, 'ore': 0}
    for i in resources: 
        if i == "h":
            toReturn['hay'] += 1
        if i == "w":
            toReturn['wood'] += 1
        if i == "o":
            toReturn['ore'] += 1
        if i == "s":
            toReturn['sheep'] += 1
        if i == "b":
            toReturn['brick'] += 1
    return toReturn

def rollDice():
    return random.randint(1, 6) + random.randint(1, 6)
    
def placeRoad(player):
    if player.roadCount < 1:   
        print("Not enough roads")
        return 0

    cursorPosition = points.getPoint(0, 0)
    cursorPosition.active = 1
    
    placed = 0
    while placed == 0:
        # print(chr(27) + "[2J")
        clear()
        print(points)
        getch = _GetchUnix()
        typed = getch.__call__()
        if typed == 'w' or ord(typed) == 65:
            cursorPosition = points.moveCursor(cursorPosition, 'up')  
        elif typed == 's' or ord(typed) == 66:
            cursorPosition = points.moveCursor(cursorPosition, 'down')  
        elif typed == 'a' or ord(typed) == 68:
            cursorPosition = points.moveCursor(cursorPosition, 'left')  
        elif typed == 'd' or ord(typed) == 67:
            cursorPosition = points.moveCursor(cursorPosition, 'right')  
        elif ord(typed) == 13:
            if cursorPosition.water == 0:
                if cursorPosition.pointType == 1 or cursorPosition.pointType == 2 or cursorPosition.pointType == 3:
                    if cursorPosition.building == 0:
                        cursorPosition.building = 1
                        cursorPosition.owner = player
                        player.roadCount -= 1
                        placed = 1
                        cursorPosition.active = 0
                        return 1

def placeSettlement(player, free):
    if player.settlementCount < 1:
        print("Not enough settlements.")
        return 0
    if not free and (player.cards.get("hay") < 1 or player.cards.get("wood") < 1 or player.cards.get("brick") or player.cards.get("sheep") < 1):
        print("Not enough cards.")
        return 0

    cursorPosition = points.getPoint(0, 0)
    cursorPosition.active = 1
    
    placed = 0
    while placed == 0:
        # print(chr(27) + "[2J")
        clear()
        print(points)
        getch = _GetchUnix()
        typed = getch.__call__()
        if typed == 'w' or ord(typed) == 65:
            cursorPosition = points.moveCursor(cursorPosition, 'up')  
        elif typed == 's' or ord(typed) == 66:
            cursorPosition = points.moveCursor(cursorPosition, 'down')  
        elif typed == 'a' or ord(typed) == 68:
            cursorPosition = points.moveCursor(cursorPosition, 'left')  
        elif typed == 'd' or ord(typed) == 67:
            cursorPosition = points.moveCursor(cursorPosition, 'right')  
        elif ord(typed) == 13:
            if cursorPosition.water == 0:
                if cursorPosition.pointType == 4:
                    if cursorPosition.building == 0:
                        cursorPosition.building = 1
                        cursorPosition.owner = player
                        player.settlementCount -= 1
                        placed = 1
                        cursorPosition.active = 0

                        if not free:
                            player.cards["hay"] = player.cards.get("hay") - 1
                            player.cards["wood"] = player.cards.get("wood") - 1
                            player.cards["brick"] = player.cards.get("brick") - 1
                            player.cards["sheep"] = player.cards.get("sheep") - 1

                        return cursorPosition
        # print(ord(typed))

def placeCity(player):
    if player.cityCount < 1:   
        print("Not enough cities.")
        return 0

    cursorPosition = points.getPoint(0, 0)
    cursorPosition.active = 1
    
    placed = 0
    while placed == 0:
        # print(chr(27) + "[2J")
        print(points)
        getch = _GetchUnix()
        typed = getch.__call__()
        if typed == 'w' or ord(typed) == 65:
            cursorPosition = points.moveCursor(cursorPosition, 'up')  
        elif typed == 's' or ord(typed) == 66:
            cursorPosition = points.moveCursor(cursorPosition, 'down')  
        elif typed == 'a' or ord(typed) == 68:
            cursorPosition = points.moveCursor(cursorPosition, 'left')  
        elif typed == 'd' or ord(typed) == 67:
            cursorPosition = points.moveCursor(cursorPosition, 'right')  
        elif ord(typed) == 13:
            if cursorPosition.water == 0:
                if cursorPosition.pointType == 4:
                    if cursorPosition.building == 1:
                        if cursorPosition.owner == player.number:
                            cursorPosition.building = 2
                            player.settlementCount += 1
                            player.cityCount -= 1
                            placed = 1
                            cursorPosition.active = 0
                            return 1
        # print(ord(typed))

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def exit(): 
    print("Thanks for playing. Exiting Console Catan.")
    time.sleep(1.5)
    clear()
    sys.exit()

# points = pointGrid(29)
# player = player(0, 'test', 'blue')
# placeSettlement(player)
# placeCity(player)

# print(points)


commandStack = []
availableCommands = commands.start

numberOfPlayers = 0
players = []
currentPlayer = None
inGame = 0

# clear()
# print(chr(27) + "[2J")
# print(bcolors.HEADER + chr(9608) + bcolors.ENDC)
print(bcolors.HEADER + "Welcome to Console Catan!" + bcolors.ENDC)
# time.sleep(1.5)
print("Type help at any time to see your available commands.")
# time.sleep(1.5)

command = input("Type start to begin a new game: ")
if command == "exit":
    exit()

points = pointGrid(29)

# print(chr(27) + "[2J")
print("Creating new game.")

inGame = 1
availableCommands = commands.creatingGame
command = input("Enter number of players between 2 and 4: ")

valid = 0
while valid == 0:
    try:
        command = int(command)
        if command < 0:
            command = input("That doesn't even make sense. Please enter a number of players that makes sense: ")
        elif command < 2:
            command = input("Please find a friend. Enter number of players when you've found one: ")
        elif command > 4:
            command = input("Console Catan does not currently support more that 4 players.\nPlease enter a number of players 4 or fewer: ")
        else:
            valid = 1
    except:
        if command == "exit":
            exit()
        if command == "help":
            command = input("Available commands: exit. Enter number of players between 2 and 4: ")
        else:
            command = input("Enter " + bcolors.UNDERLINE +"number" + bcolors.ENDC + " of players between 2 and 4: ")

numberOfPlayers = command

print("Creating players.\n")
for item in range(numberOfPlayers):
    name = 0
    command = input(bcolors.HEADER + "Player " + str(item + 1) + bcolors.ENDC + "\nEnter your name: ")
    while name == 0:
        if command == "help" or command == "exit":
            command = input("That word is reserved. Please try a different name: ")
        else: 
            name = command
    availableCommands = commands.choosingColor
    color = 0
    print("Please enter a color [ ", end="")
    for canChoose in commands.choosingColor:
        print(canChoose + " ", end="") 
    command = input("]: ")
    while color == 0:
        checkCommand(command)
        print(command)
        commands.choosingColor.remove(command)
        color = command
    print(item)
    players.append(player(item, name, color))

print(chr(27) + "[2J")
print("Creating new game.")
print("Placing Settlements and Roads\n")
for item in range(numberOfPlayers):
    player = players[item]
    print(player.color)
    print(bcolors.HEADER + "Player " + str(item + 1) + bcolors.ENDC + "\nPlace your settlement.\nUse arrow keys or wasd to move the cursor. Press enter to place settlement.")
    placeSettlement(player, True)
    print(bcolors.HEADER + "Player " + str(item + 1) + bcolors.ENDC + "\nPlace your road.\nUse arrow keys or wasd to move the cursor. Press enter to place road.")
    placeRoad(player)
    print(points)

for item in range(numberOfPlayers):
    player = players[item]
    print(player.color)
    print(bcolors.HEADER + "Player " + str(item + 1) + bcolors.ENDC + "\nPlace your second settlement.\nUse arrow keys or wasd to move the cursor. Press enter to place settlement.")
    position = placeSettlement(player, True)
    # give cards
    cards = getResources(position, points)
    player.cards = cards
    print(bcolors.HEADER + "Player " + str(item + 1) + bcolors.ENDC + "\nPlace your second road.\nUse arrow keys or wasd to move the cursor. Press enter to place road.")
    placeRoad(player)
    print(points)
    
print("Beginning game.")

currentPlayerIndex = 0

while True: 
    currentPlayer = players[currentPlayerIndex]

    # for currentPlayer in players:
    print(currentPlayer.name + ", it is your turn.\n")
    print("Cards: " + currentPlayer.getCards())
    command = input("Commands: (p)lay dev card, (r)oll")

    if command == "p":
        print("Dev cards: " + currentPlayer.getDevCards())
        command = input("")
    if command == "r":
        print("Roll: " + str(rollDice()))
        
    command = input("Commands (b)uild, (t)rade, buy (d)ev card, (e)nd turn: ")

    # command = input("Cards \
    #     hay: " + currentPlayer.cards.get('hay') + " \n\
    #     sheep: " + currentPlayer.cards.get('sheep') + " \n\
    #     wood: " + currentPlayer.cards.get('wood') + " \n\
    #     brick: " + currentPlayer.cards.get('brick') + " \n\
    #     ore: " + currentPlayer.cards.get('ore') + " \n\
    #     Dev Cards: " + getDevCards(currentPlayer) + " \n\
    #     Commands (b)uild, (t)rade, buy (d)ev card, (p)lay dev card, (e)nd turn: ")

    # user selected "build"
    if (command == "b"):
        commandTwo = input("(Building) Cards: " + str(player.cards) + ".\nCommands: (s)ettlement, (c)ity, (r)oad, (e)xit: ")
        if commandTwo == "s":
            print(bcolors.HEADER + "Player " + str(item + 1) + bcolors.ENDC + "\nPlace your settlement.\nUse arrow keys or wasd to move the cursor. Press enter to place settlement.")
            placeSettlement(player, False)
        # if commandTwo == "c":
        # if commandTwo == "r":
        # if commandTwo == "e":
    # user selected "trade"
    elif (command == "t"):
        commandTwo = input("(Trade) Trade with (p)layer or por(t) or (e)xit: ")
    # user selected to trade with play
    if (commandTwo == "p"):
        commandThree = input("(Trade>Player) Cards hay: 0, sheep: 0, wood: 0, brick: 0, ore: 0.\nEnter player to trade with, (l)ist players, or (e)xit: ")

    if command == "e":
        currentPlayerIndex += 1

# print("\nEntered: " + command)