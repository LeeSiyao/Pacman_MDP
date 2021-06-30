# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util


class MDPAgent(Agent):
    """
       Author: Siyao Li           Student_ID: K20113549
       Major: robotics            Email: k20113549@kcl.ac.uk
    """

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"
        # Gets run after an MDPAgent object is created and once there is
        # game state to access.

        # Lists to store useful information
        self.visited = []
        self.foodMap = []
        self.capsuleMap = []
        self.wallMap = []

    def registerInitialState(self, state):
        print "Running MDPAgent Pacman!"

    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

        # Clear all storage data before next time run
        self.visited = []
        self.foodMap = []
        self.capsuleMap = []
        self.wallMap = []

    def mapSize(self, state):
        """use this function to get the size of the map
        aip.corners return the coordinate of corners' positions
        zip it into two lists: one contains the values of X, the other one contains values of Y
        max(layout[0]) returns the maximum value of x, which represent the width of layout
        max(layout[1]) returns the maximun value of y, which represent the height of layout
        """
        layout = zip(*(api.corners(state)))
        return max(layout[0]), max(layout[1])

    def getMapValue(self, state):
        """use this function to update the map value
        """

        # Get the information of the map (the position of foods, ghost, capsules, walls and pacman)
        food = api.food(state)
        walls = api.walls(state)
        capsules = api.capsules(state)
        ghosts = api.ghosts(state)
        pacman = api.whereAmI(state)

        # update new positions of pacman
        if pacman not in self.visited:
            self.visited.append(pacman)

        # update new foods
        for n in food:
            if n not in self.foodMap:
                self.foodMap.append(n)

        # update new capsules
        for n in capsules:
            if n not in self.capsuleMap:
                self.capsuleMap.append(n)

        # update the information of walls
        for n in walls:
            if n not in self.wallMap:
                self.wallMap.append(n)

        # create a dictionary to contain the value of the map
        # set the value of capsules as 5
        # set the value of food as 5
        # use '#' to represent walls
        MapValue = {}
        MapValue.update(dict.fromkeys(self.foodMap, 50))
        MapValue.update(dict.fromkeys(self.capsuleMap, 50))
        MapValue.update(dict.fromkeys(self.wallMap, '#'))

        # get the size of the map
        size = self.mapSize(state)

        # update the initial values of map as 0
        for i in range(size[0]):
            for j in range(size[1]):
                if (i, j) not in MapValue.keys():
                    MapValue[(i, j)] = 0

        # set the value of eaten foods as 0
        for n in self.foodMap:
            if n in self.visited:
                MapValue[n] = 0
        # set the value of eaten capsules as 0
        for n in self.capsuleMap:
            if n in self.visited:
                MapValue[n] = 0
        # Set the position of ghosts as -100
        if ghosts:
            for g in ghosts:
                MapValue[(round(g[0]), round(g[1]))] = -1000
                # output the value of the whole map
        return MapValue

    def utilityValue(self, position, map):
        """Calculate the utilities for four directions
        """

        x = position[0]
        y = position[1]  # coordinate of current position

        north = (x, y + 1)
        south = (x, y - 1)
        west = (x - 1, y)
        east = (x + 1, y)
        stay = (x, y)

        # set a list to store utilities of four directions
        utiluties = {"n_util": 0.0, "s_util": 0.0, "e_util": 0.0, "w_util": 0.0}

        # possibility of four direction: 0.7 (for target direction), 0.1, 0.1, 0.1
        # target direction: north
        if map[north] != '#':
            n_util = (0.7 * map[north])
        else:
            n_util = (0.7 * map[stay])  # use the utility of stay represent wall
        if map[east] != '#':
            n_util += (0.1 * map[east])
        else:
            n_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[west] != '#':
            n_util += (0.1 * map[west])
        else:
            n_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[south] != '#':
            n_util += (0.1 * map[south])
        else:
            n_util += (0.1 * map[stay])  # use the utility of stay represent wall

        utiluties["n_util"] = n_util

        # target direction: south
        if map[south] != '#':
            s_util = (0.7 * map[south])
        else:
            s_util = (0.7 * map[stay])  # use the utility of stay represent wall
        if map[east] != '#':
            s_util += (0.1 * map[east])
        else:
            s_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[west] != '#':
            s_util += (0.1 * map[west])
        else:
            s_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[north] != '#':
            s_util += (0.1 * map[north])
        else:
            s_util += (0.1 * map[stay])  # use the utility of stay represent wall

        utiluties["s_util"] = s_util

        # target direction: west
        if map[west] != '#':
            w_util = (0.7 * map[west])
        else:
            w_util = (0.7 * map[stay])  # use the utility of stay represent wall
        if map[north] != '#':
            w_util += (0.1 * map[north])
        else:
            w_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[south] != '#':
            w_util += (0.1 * map[south])
        else:
            w_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[east] != '#':
            w_util += (0.1 * map[east])
        else:
            w_util += (0.1 * map[stay])  # use the utility of stay represent wall

        utiluties["w_util"] = w_util

        # target direction: east
        if map[east] != '#':
            e_util = (0.7 * map[east])
        else:
            e_util = (0.7 * map[stay])  # use the utility of stay represent wall
        if map[north] != '#':
            e_util += (0.1 * map[north])
        else:
            e_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[south] != '#':
            e_util += (0.1 * map[south])
        else:
            e_util += (0.1 * map[stay])  # use the utility of stay represent wall
        if map[west] != '#':
            e_util += (0.1 * map[west])
        else:
            e_util += (0.1 * map[stay])  # use the utility of stay represent wall

        utiluties["e_util"] = e_util

        return utiluties

    def valueIterationSmall(self, state, map):
        """
        use this function to further set the value of position which is close to ghost but
        worthy for pacman to collect foods or capsules
        especially for the small type of layout
        """
        reward = -1.0  # set the value ana gamma which will use in the Bellman Equation
        gamma = 0.95
        # set iteration times to 100
        loops = 100

        # Get the information of the map (the position of foods, ghost, capsules, walls)
        capsules = api.capsules(state)
        walls = api.walls(state)
        ghosts = api.ghosts(state)
        food = api.food(state)

        risk = []  # set a list to store the positions near ghost
        for g in ghosts:
            ghostPosition = (round(g[0]), round(g[1]))
            # set a list to represent whether food position is wall or not
            # 8 direction which contains north, south, west, east, northeast, northwest, southeast and southwest
            W_all = 8 * [0]
            for i in range(3):
                # east
                dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1]))
                if dangerousPosition not in risk and W_all[0] == 0:
                    # if this position is wall we don't need to consider it as a dangerous place
                    # because walls defend us from ghost
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[0] = '#'  # set the walls' values

                # west
                dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1]))
                if dangerousPosition not in dangerousPosition and W_all[1] == 0:
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[1] = '#'  # set the walls' values

                # north
                dangerousPosition = (int(ghostPosition[0]), int(ghostPosition[1]) + i)
                if dangerousPosition not in risk and W_all[2] == 0:
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[2] = '#'  # set the walls' values

                # south
                dangerousPosition = (int(ghostPosition[0]), int(ghostPosition[1]) - i)
                if dangerousPosition not in risk and W_all[3] == 0:
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[3] = '#'  # set the walls' values

                # northeast
                dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1] + i))
                if dangerousPosition not in risk and W_all[4] == 0:
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[4] = '#'  # set the walls' values

                # northwest
                dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1] + i))
                if dangerousPosition not in risk and W_all[5] == 0:
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[5] = '#'  # set the walls' values

                # southeast
                dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1] - i))
                if dangerousPosition not in risk and W_all[6] == 0:
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and (
                            dangerousPosition) not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[6] = '#'  # set the walls' values

                # southwest
                dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1] - i))
                if dangerousPosition not in risk and W_all[7] == 0:
                    risk.append(dangerousPosition)
                    if i <= 3 and dangerousPosition not in walls and (
                            dangerousPosition) not in ghosts and dangerousPosition not in food and dangerousPosition not in capsules:
                        map[dangerousPosition] = -700 + 15 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[7] = '#'  # set the walls' values

        # If there is food or capsule not near the ghost. The coordinate no need to update
        normalFood = []
        for f in food:
            if f not in risk:
                normalFood.append(f)

        for f in capsules:
            if f not in risk:
                normalFood.append(f)

        size = self.mapSize(state)
        while loops > 0:
            current_map = map
            for i in range(size[0]):
                for j in range(size[1]):
                    # Iterate the value map by Bellman equation
                    if (i, j) not in walls and (i, j) not in normalFood and (i, j) not in ghosts and (
                            i, j) not in capsules:
                        utilities = self.utilityValue((i, j), current_map)
                        # Take the maximum utility of four directions as the utility at (i,j)
                        map[(i, j)] = reward + gamma * max(utilities.values())
            loops -= 1
        return map

    def valueIterationMedium(self, state, map):
        """
        use this function to further set the value of position which is close to ghost but
        worthy for pacman to collect foods or capsules
        especially for the medium type of layout
        """

        # Get the information of the map (the position of foods, ghost, capsules, walls)
        capsules = api.capsules(state)
        walls = api.walls(state)
        ghosts = api.ghosts(state)
        food = api.food(state)

        reward = -1  # reward for every state
        gamma = 0.9  # discount factor
        # set iteration times to 50
        loops = 50

        # set a list to store the positions near ghost
        risk = []

        for g in ghosts:
            # The ghosts is in another thread, there might be float number
            ghostPosition = (round(g[0]), round(g[1]))
            # set a list to represent whether food position is wall or not
            # 8 direction which contains north, south, west, east, northeast, northwest, southeast and southwest
            W_all = 8 * [0]
            for i in range(3):
                # east
                dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1]))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[1] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[1] = '#'  # set the walls' values

                # west
                dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1]))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[2] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[2] = '#'  # set the walls' values

                # north
                dangerousPosition = (int(ghostPosition[0]), int(ghostPosition[1] + i))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[3] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[3] = '#'  # set the walls' values

                # northwest
                dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1] + i))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[5] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[5] = '#'  # set the walls' values
                # northeast
                dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1] + i))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[4] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[4] = '#'  # set the walls' values

                # northwest
                dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1] + i))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[5] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[5] = '#'  # set the walls' values

                # southeast
                dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1] - i))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[6] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[6] = '#'  # set the walls' values

                # southwest
                dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1] - i))
                if dangerousPosition not in walls and dangerousPosition not in ghosts and dangerousPosition not in risk and \
                        W_all[7] == 0:
                    map[dangerousPosition] = -70 + 10 * i  # set the values of dangerous places
                    if dangerousPosition in walls:
                        W_all[7] = '#'  # set the walls' values

                # the dangerous position is a 7*7 square in medium grid
                for j in range(3):
                    dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1] + j))
                    if dangerousPosition not in risk:
                        risk.append(dangerousPosition)
                    dangerousPosition = (int(ghostPosition[0] + i), int(ghostPosition[1] - j))
                    if dangerousPosition not in risk:
                        risk.append(dangerousPosition)
                    dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1] + j))
                    if dangerousPosition not in risk:
                        risk.append(dangerousPosition)
                    dangerousPosition = (int(ghostPosition[0] - i), int(ghostPosition[1] - j))
                    if dangerousPosition not in risk:
                        risk.append(dangerousPosition)

        # If there is food or capsule not near the ghost. The coordinate no need to update
        normalFood = []
        for f in food:
            if f not in risk:
                normalFood.append(f)

        for f in capsules:
            if f not in risk:
                normalFood.append(f)

        size = self.mapSize(state)
        while loops > 0:
            current_map = map
            for i in range(size[0]):
                for j in range(size[1]):
                    # Iterate the value map by Bellman equation
                    if (i, j) not in walls and (i, j) not in normalFood and (i, j) not in ghosts and (
                            i, j) not in capsules:
                        utilities = self.utilityValue((i, j), current_map)
                        # Take the maximum utility of four directions as the utility at (i,j)
                        map[(i, j)] = reward + gamma * max(utilities.values())
            loops -= 1
        return map

    def moveDirection(self, state, map):
        """use the valuemap to choose the move direction
        """
        pacman = api.whereAmI(state)  # get pacman position
        utilities = self.utilityValue(pacman, map);  # get pacman's value map
        maxValue = max(zip(utilities.values(), utilities.keys()))  # get the value of maximum utility and it's direction

        # choose the direction to move
        if maxValue[1] == 'n_util':
            return Directions.NORTH
        if maxValue[1] == 's_util':
            return Directions.SOUTH
        if maxValue[1] == 'w_util':
            return Directions.WEST
        if maxValue[1] == 'e_util':
            return Directions.EAST

    def getAction(self, state):
        """Get Action of pacman
        """
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        width, height = self.mapSize(state)  # get the size of layout
        Init_map = self.getMapValue(state)  # get the initial map

        if width >= 10 and height >= 10:
            action_map = self.valueIterationMedium(state, Init_map)  # the iterated map of medium layout
        else:
            action_map = self.valueIterationSmall(state, Init_map)  # the iterated map of small layout
        # Make move
        return api.makeMove(self.moveDirection(state, action_map), legal)
