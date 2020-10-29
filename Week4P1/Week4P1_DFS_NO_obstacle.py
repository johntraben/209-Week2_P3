# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:21:51 2020

@author: fishy
"""

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.visited = False

    def addNeighbor(self,nbr):
        self.connectedTo[nbr] = 1

    def getConnections(self):
        return self.connectedTo.keys()

    def setVisited(self):
        self.visited = True
        
    def setUnvisited(self):
        self.visited = False


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t])

    def getVertices(self):
        return self.vertList.keys()

    

def knightGraph(bdSize):
    ktGraph = Graph()
    for row in range(bdSize):
       for col in range(bdSize):
           nodeId = posToNodeId(row,col,bdSize)
           newPositions = genLegalMoves(row,col,bdSize)
           for e in newPositions:
               nid = posToNodeId(e[0],e[1],bdSize)
               ktGraph.addEdge(nodeId,nid)
    return ktGraph

def posToNodeId(row, column, board_size):
    return (row * board_size) + column

def nodeIdToPos(ID, board_size):
    row = ID // board_size
    column = ID % board_size
    return (row,column)


def genLegalMoves(x,y,bdSize):
    newMoves = []
    moveOffsets = [(-1,-2),(-1,2),(-2,-1),(-2,1),
                   ( 1,-2),( 1,2),( 2,-1),( 2,1)]
    for i in moveOffsets:
        newX = x + i[0]
        newY = y + i[1]
        if legalCoord(newX,bdSize) and \
                        legalCoord(newY,bdSize):
            newMoves.append((newX,newY))
    return newMoves

def legalCoord(x,bdSize):
    if x >= 0 and x < bdSize:
        return True
    else:
        return False
    
def knightPath(n,path,u,goal):
        u.setVisited()
        path.append(u.id)
        if u != goal:
            nbrList = list(u.getConnections())
            i = 0
            done = False
            while i < len(nbrList) and not done:
                if nbrList[i].visited == False:
                    done = knightPath(n+1, path, nbrList[i], goal)
                i = i + 1
            if not done:  # prepare to backtrack
                path.pop()
                u.setUnvisited()
        else:
            done = True
            print("Following is a path:")
            for i in path:
                print(nodeIdToPos(i, 8))
        return done    

    
boardGraph = knightGraph(8)
x = 8
y = 8
while not(legalCoord(x,8)) or not(legalCoord(y,8)):
    x , y = [int(k) for k in input("Enter Starting Postion on chessboard (pair of integer from 0 to 7 ,seperated by space):").split()]
    
u = boardGraph.getVertex(posToNodeId(x,y,8))   

x = 8
y = 8
while not(legalCoord(x,8)) or not(legalCoord(y,8)):
    x , y = [int(k) for k in input("Enter Final Postion on chessboard (pair of integer from 0 to 7 ,seperated by space):").split()]
    

goal = boardGraph.getVertex(posToNodeId(x,y,8))

path = []

knightPath(0, path, u, goal)

