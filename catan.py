from __future__ import print_function
from collections import deque
import math

class bcolors:
    OKBLUE = '\033[94m'
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	
class coord(object):
	# initialize the coordinate object
	#
	# @param x        the x coordinate
	# @param y        the y coordinate
	# @param water    0 if coordinate is on land, 1 if in water
	# @param pointType     0 if none, 1 if road up type, 2 if road flat type, 3 if road down type, 4 if building type 
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

class board():
    def __init__(self, points, tiles):
        self.points = points
        self.tiles = tiles
		    
class player():
    def __init__(self, name):
        self.name = name
        self.cards = {'hay': 0, 'sheep': 0, 'wood': 0, 'brick': 0, 'ore': 0}
        self.points = 0
        self.settlemtnCount = 5
        self.cityCount = 4
        self.roadCount = 15
        self.devCards = []
    

size = 29
width = size
height = int(math.floor(width/2.0))    #14
middle = int(math.floor(height/2.0))   #7
pointTypePattern = deque([3, 4, 2, 4, 1, 0, 0, 0])
# 1, 0, 0, 0, 1, 2, 1, 2,
# 42410003


# print(middle)
points = []
for y in range(height+1):
    pointTypePattern.rotate(4)
    points.append([])
    for x in range(width):
        water = 0
        pointType = pointTypePattern[x%8]   
        
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
        

for y in range(height+1):
    if (y != 0):
        print("\n", end="")
    for x in range(width):
        if (points[y][x].water == 1):
            color = bcolors.OKBLUE
        else:
            color = bcolors.ENDC
        
        if (points[y][x].pointType == 0):
            toPrint = " "
        elif (points[y][x].pointType == 1):
            toPrint = "/"
        elif (points[y][x].pointType == 2):
            toPrint = "_"
        elif (points[y][x].pointType == 3):
            toPrint = "\\"
        else:
            if (points[y][x].building == 0):
                toPrint = "_"
            elif (points[y][x].building == 1):
                toPrint = "."
            elif (points[y][x].building == 2):
                toPrint = ","
        print(color + toPrint + bcolors.ENDC, end="")

print("\n", end="")


# myBuildCoord = buildCoord(0, 0, 0)
# print myBuildCoord.x
# print myBuildCoord.y
# print myBuildCoord.building
# print myBuildCoord.owner

