from __future__ import print_function
from collections import deque
import math
import sys
import time

class bcolors:
    OKBLUE = '\033[94m'
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class commands:
    start = ['start', 'exit']
    creatingGame = ['exit']
    choosingColor = ['blue', 'green', 'red', 'yellow', 'exit']

	
class coord(object):
	# initialize the coordinate object
	#
	# @param x        the x coordinate
	# @param y        the y coordinate
	# @param water    0 if coordinate is on land, 1 if in water
	# @param pointType     0 if none, 1 if road up type, 2 if road flat type, 3 if road down type, 4 if building type, 5 if resource type
	# @param building 0 if no building, 1 if road or settlement, 2 if city
	# @param owner    the ID of the player who owns the building if any
	def __init__(self, x, y, water, pointType, building=0, owner=None):
		self.x = x
		self.y = y
		self.water = water
		self.pointType = pointType
		self.building = building
		self.owner = owner

	# overwrite the print function
    #
	# @return will return the coordinate in format (x, y)
	def __str__(self):
		return "(" + str(self.y) + ", " + str(self.x) + ") water: " + str(self.water) + " pointType: " + str(self.pointType) + " building: " + str(self.building)

class tilePart(object):
	def __init__(self, x, y, ownedCoords=[]):
		self.x = x
		self.y = y
		self.ownedCoords = ownedCoords
        
class tileWhole():
	def __init__(self, topTile, bottomTile, resource, shutdown=0):
		self.topTile = topTile
		self.bottomTile = bottomTile
		self.resource = resource
		self.shutdown = shutdown

class pointGrid():
    def __init__(self, size):
        self.size = size
        width = size
        height = int(math.floor(width/2.0))    #14
        middle = int(math.floor(height/2.0))   #7
        pointTypePattern = deque([3, 4, 2, 4, 1, 0, 5, 0])

        points = []
        for y in range(height+1):
            pointTypePattern.rotate(4)
            points.append([])
            for x in range(width):
                water = 0
                pointType = pointTypePattern[x%8]   
                
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
                    
                point = coord(x, y, water, pointType)
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
                    color = bcolors.OKBLUE
                else:
                    color = bcolors.ENDC
                
                # if empty or resource type
                if (points[y][x].pointType == 0):
                    toPrint = " "
                # if road up type
                elif (points[y][x].pointType == 1):
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
                        toPrint = "."
                    # if city
                    elif (points[y][x].building == 2):
                        toPrint = ","
                elif (points[y][x].pointType == 5):
                    toPrint = " "
                toReturn += color + toPrint + bcolors.ENDC
        
        return toReturn

class board():
    def __init__(self, points):
        print("")
		    
class player():
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.cards = {'hay': 0, 'sheep': 0, 'wood': 0, 'brick': 0, 'ore': 0}
        self.points = 0
        self.settlementCount = 5
        self.cityCount = 4
        self.roadCount = 15
        self.devCards = []
    
def checkCommand(command):
    commandStack.append(command)
    if (command == "help"):
        commandStack.pop()
        print("Available commands: ", end="")
        for item in iter(availableCommands):
            print(item + " ", end="")
        print("")
        # time.sleep(1.5)
        command = raw_input("Enter one of the available commands: ")
        checkCommand(command)
    elif (command == "exit"):
        if inGame:
            command = raw_input("Any unsaved progress will be lost; are you sure you want to quit? y/n: ")
            valid = 0
            while valid == 0:
                if command == "y":
                    print("Thanks for playing. Exiting Console Catan.")
                    time.sleep(1.5)
                    print(chr(27) + "[2J")
                    sys.exit()
                elif command == "n":
                    print("Your game probably just broke. Sorry.")
                    return 0
                else:
                    command = raw_input("Please enter y or n: ")
        else:
            print("Thanks for playing. Exiting Console Catan.")
            time.sleep(1.5)
            print(chr(27) + "[2J")
            sys.exit()
    else:
        validCommand = 0
        for item in iter(availableCommands):
            if (command == item):
                validCommand = 1
                break
        if validCommand == 0:
            commandStack.pop()
            newCommand = raw_input("Command not available. Type help to see available commands or enter valid command: ")
            checkCommand(newCommand)
        else:
            return 1




commandStack = []
availableCommands = commands.start

numberOfPlayers = 0
players = []
currentPlayer = None
inGame = 0

print(chr(27) + "[2J")
print(bcolors.HEADER + "Welcome to Console Catan!" + bcolors.ENDC)
# time.sleep(1.5)
print("Type help at any time to see your available commands.")
# time.sleep(1.5)
command = raw_input("Type start to begin a new game: ")

print(chr(27) + "[2J")
print("Creating new game.")

inGame = 1
availableCommands = commands.creatingGame
command = raw_input("Enter number of players between 2 and 4: ")

valid = 0
while valid == 0:
    try:
        command = int(command)
        if command < 0:
            command = raw_input("That doesn't even make sense. Please enter a number of players that makes sense: ")
        elif command < 2:
            command = raw_input("Please find a friend. Enter number of players when you've found one: ")
        elif command > 4:
            command = raw_input("Console Catan does not currently support more that 4 players.\nPlease enter a number of players 4 or fewer: ")
        else:
            valid = 1
    except:
        if command == "exit":
            print("Thanks for trying. Exiting Console Catan.")
            time.sleep(1.5)
            print(chr(27) + "[2J")
            sys.exit()
        if command == "help":
            command = raw_input("Available commands: exit. Enter number of players between 2 and 4: ")
        else:
            command = raw_input("Enter " + bcolors.UNDERLINE +"number" + bcolors.ENDC + " of players between 2 and 4: ")

numberOfPlayers = command

print("Creating players.\n")
for item in range(numberOfPlayers):
    name = 0
    command = raw_input(bcolors.HEADER + "Player " + str(item + 1) + bcolors.ENDC + "\nEnter your name: ")
    while name == 0:
        if command == "help" or command == "exit":
            command = raw_input("That word is reserved. Please try a different name: ")
        else: 
            name = command
    availableCommands = commands.choosingColor
    color = 0
    print("Please enter a color [ ", end="")
    for canChoose in commands.choosingColor:
        print(canChoose + " ", end="") 
    command = raw_input("]: ")
    while color == 0:
        checkCommand(command)
        print(command)
        commands.choosingColor.remove(command)
        color = command
    players.append(player(name, color))




# points = pointGrid(29)
# print(points)


# command = raw_input("Player: " + "" + ". Cards hay: 0, sheep: 0, wood: 0, brick: 0, ore: 0. Dev Cards: none.\n" + "Commands (b)uild, (t)rade, buy (d)ev card, (e)nd turn: ")

# # user selected "build"
# if (command == "b"):
#     commandTwo = raw_input("(Building) Cards hay: 0, sheep: 0, wood: 0, brick: 0, ore: 0.\nCommands: (s)ettlement, (c)ity, (r)oad, (e)xit: ")
# # user selected "trade"
# elif (command == "t"):
#     commandTwo = raw_input("(Trade) Trade with (p)layer or por(t) or (e)xit: ")
#     # user selected to trade with play
#     if (commandTwo == "p"):
#         commandThree = raw_input("(Trade>Player) Cards hay: 0, sheep: 0, wood: 0, brick: 0, ore: 0.\nEnter player to trade with, (l)ist players, or (e)xit: ")

        
# print("\nEntered: " + command)