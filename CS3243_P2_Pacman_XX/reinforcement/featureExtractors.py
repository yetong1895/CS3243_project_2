# featureExtractors.py
# --------------------
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


"Feature extractors for Pacman game states"

from game import Directions, Actions
import util, math

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features

class NewExtractor(FeatureExtractor):
    """
    Design you own feature extractor here. You may define other helper functions you find necessary.

    """

    def closestCapsule(self, pos, capsule, walls):
        """
        closestCapsule -- this is similar to the function that we have
        worked on in the search project; here its all in one place
        """
        fringe = [(pos[0], pos[1], 0)]
        expanded = set()
        while fringe:
            pos_x, pos_y, dist = fringe.pop(0)
            if (pos_x, pos_y) in expanded:
                continue
            expanded.add((pos_x, pos_y))
            # if we find a food at this location then exit
            if (pos_x, pos_y) in capsule:
                return dist
            # otherwise spread out from the location to its neighbours
            nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
            for nbr_x, nbr_y in nbrs:
                fringe.append((nbr_x, nbr_y, dist+1))
        # no capsule found
        return None

    def closestGhost(self, pos, ghosts, walls):
        """
        closestGhost returns the distance to the closest ghost
        """
        fringe = [(pos[0], pos[1], 0)]
        expanded = set()
        while fringe:
            pos_x, pos_y, dist = fringe.pop(0)
            if (pos_x, pos_y) in expanded:
                continue
            expanded.add((pos_x, pos_y))
            # if we find a food at this location then exit
            if (pos_x, pos_y) in ghosts:
                return dist
            # otherwise spread out from the location to its neighbours
            nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
            for nbr_x, nbr_y in nbrs:
                fringe.append((nbr_x, nbr_y, dist+1))
        # no ghost found
        return None

    def howTunnel(self, pos, oriPos, ghosts, walls):
        """
        howTunnel returns a value of "how tunnel" is entering a tunnel with an active ghost
        """   
        nbrs = Actions.getLegalNeighbors(pos, walls)
        numberLegalMove = 0
        for nbr_x, nbr_y in nbrs:
            if (nbr_x, nbr_y) in ghosts:
                continue
            numberLegalMove += 1

        if numberLegalMove < 2:
            return 2.0

        if numberLegalMove == 2:
            return 1.0
            
        else:
            return 0.0
            
        # fringe = [(pos[0], pos[1], 0)]
        # expanded = set()
        #expanded.add(oriPos)

        # while fringe:
        #     pos_x, pos_y, dist = fringe.pop(0)
        #     if (pos_x, pos_y) in expanded:
        #         continue
        #     expanded.add((pos_x, pos_y))

        #     # otherwise spread out from the location to its neighbours
        #     nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        #     numberLegalMove = 0

        #     for nbr_x, nbr_y in nbrs:
        #         if (nbr_x, nbr_y) in ghosts:
        #             continue
        #         numberLegalMove += 1
        #         fringe.append((nbr_x, nbr_y, dist+1))
            
        #     if numberLegalMove < 2:
        #         return dist * 5

        #     if numberLegalMove >= 3:
        #         return dist

        #return 0.0
        
    def getGhostPos(self, ghoststates):
        activePositions = []
        scaredPositions = []

        for ghost in ghoststates:
            isScared = ghoststates[0].scaredTimer > 0
            if isScared:
                scaredPositions.append(ghost.getPosition())
            else :
                activePositions.append(ghost.getPosition())

        return activePositions, scaredPositions

    def getFeatures(self, state, action):
        """
        Returns features for Pacman:
        - whether food will be eaten 
        - inverse min distance of capsule
        - inverse min distance of food
        - whether a ghost collision is imminent
        - number of active ghost nearby
        - number of scared ghost nearby
        - inverse min distance to nearest active ghost
        - inverse min distance to nearest scared ghost
        - whether it's eating a capsule proportional to the amount of ghost scared
        - whether it's entering a tunnel proportional to it's length and proportional to amt of active ghost
        """
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        capsules = state.getCapsules()
        ghoststates = state.getGhostStates()
        ghostPos = self.getGhostPos(ghoststates)
        activeGhostPos = ghostPos[0]
        scaredGhostPos = ghostPos[1]

        #idea: use distance from ghost and negate it depending on whether they are scared

        #idea: use a linear combination to represent distance to food, currently will leave one portion of food alone
        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)
        nextPos = next_x, next_y
    
        # count the number of active ghosts 1 step away from player
        features["#-of-active-ghosts-1-step-away"] = sum(nextPos in Actions.getLegalNeighbors(g, walls) for g in activeGhostPos)   
        
        if nextPos in activeGhostPos:
            features["collide-with-ghost"] = 1.0

        # the distance to the nearest active ghost
        #idea: give the distance to other ghost as well as a weighted sum
        distGhost = self.closestGhost(nextPos, activeGhostPos, walls)
        if distGhost is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-active-ghost"] = 1 / (float (distGhost) + 1)

        #whether it's entering a tunnel proportional to it's length and proportional to amt of active ghost
        tunnelWeight = self.howTunnel(nextPos, (x, y), activeGhostPos, walls)
        if tunnelWeight != 0 and len(activeGhostPos) != 0:
            features["#value-of-tunnel-multiplied-active-ghost"] = (len(activeGhostPos) * tunnelWeight) / (walls.width * walls.height) 
        
        
        # The rest of the features only apply when there is no danger of ghost
        if features["collide-with-ghost"] == 0.0: 
            #then add the food feature
            if food[next_x][next_y]:
                features["eats-food"] = 1.0

            distGhostScared = self.closestGhost((next_x, next_y), scaredGhostPos, walls)
            if distGhostScared is not None:
                # make the distance a number less than one otherwise the update
                # will diverge wildly
                features["closest-scared-ghost"] = 1 / (float (distGhostScared) + 1)

            # count the number of scared ghosts 1 step away from player
            features["#-of-scared-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in scaredGhostPos)

            # if there is no danger of ghosts 
            #if (next_x, next_y) in scaredGhostPos:
            #    features["eats-ghost"] = 1.0
                     
            distFood = closestFood((next_x, next_y), food, walls)
            if distFood is not None:
                # make the distance a number less than one otherwise the update
                # will diverge wildly
                features["closest-food"] = 1 / (float(distFood) + 1)

            distCapsule = self.closestCapsule((next_x, next_y), capsules, walls)
            if distCapsule is not None:
                # make the distance a number less than one otherwise the update
                # will diverge wildly
                features["closest-capsule"] = 1 / (float(distCapsule) + 1)

                # whether it's eating a capsule based on how many is scared
                #if len(activeGhostPos) == 0:
                #   features["eating-capsule-when-ghost-scared"] = len(scaredGhostPos) / len(ghoststates)

        features.divideAll(10.0)
        return features


        
