"""
Created on Fri Feb  9 17:39:03 2018

@author: Vishal
Final Code for the Practical including Task 1 and Task 2
"""
import googlemaps
from queue import Queue

gmaps = googlemaps.Client(key = 'AIzaSyB8Sjq1wYpnC2mKqyheCNeeTIpZKNVKovI')

class Node(object): #needed for new style class
    #class will only hold a value which will be title and children nodes
    def __init__(self, value):
        self.value = value
        self.children = []
        self.distances = [] # will be parallel to children list
    """
    returns index of node(value) in self.children
    """
    def find(self, value):
        i = 0
        while (i != len(self.children) and self.children[i].value != value):
            i += 1
        return i
    
    def hasChild(self, value):
        if (self.find(value) == len(self.children)):
            return False
        return True
      
    #don't clutter the tree unnecessarily since there is no delete method    
    def addChild(self, child):
        if (self.find(child.value) == len(self.children)): # not found
            self.children.append(child)
    
class Tree(object): #will be structured like a graph
    def __init__(self):
        self.nodes = []
        self.root = None
        self.updateFlag = False
    
    """
    checks if the given value node already exists in tree
    """
    def isDuplicate(self, value):
        i = 0
        while (i < len(self.nodes) and self.nodes[i].value != value):
            i += 1
        if (i == len(self.nodes)):
            return False
        else:
            return True
    """
    inserts into completely connected graph
    """
    def insert(self, value):
        #create a new root(Starting location) if needed
        if (self.root == None):
            self.root = Node(value)
            self.nodes.append(self.root)
            return
        """
        # if not root then each node in graph needs a link to newly added node
        # new node also needs a link to each existing node
        # new node then needs to be added to the existing nodes list
        # don't clutter graph with duplicates
        """
        if (not self.isDuplicate(value)):
            temp = Node(value)
            for i in range(len(self.nodes)):
                self.nodes[i].addChild(temp)
                temp.addChild(self.nodes[i])
            self.nodes.append(temp)
            self.updateFlag = True
    """
    sets correct distances in each node
    """
    def updateDistances(self):
        for i in range(0, len(self.nodes)):
            temp = []
            for j in range(0, len(self.nodes)):
                if (i == j):
                    continue
                dist_dict = gmaps.distance_matrix(self.nodes[i].value, self.nodes[j].value)
                temp.insert(self.nodes[i].find(self.nodes[j].value), dist_dict["rows"][0]["elements"][0]["distance"]["value"])
            self.nodes[i].distances = temp
            #overwrite previous distances array
        self.updateFlag = False
    
    """
    returns actual node object that has value
    """
    def find(self, value):
        i = 0
        while (i != len(self.nodes) and self.nodes[i].value != value):
            i += 1
        if (i == len(self.nodes)):
            return None
        return self.nodes[i]
    
    """
    prints all children of node(value) with distance
    """
    def printChildren(self, node):
        print(node.value + '\n')
        for i in range (len(node.children)):
            print(node.children[i].value)
            if (node.distances):
                print(node.distances[i])
        print()    
    
    """
    returns deep copy of tree
    """
    def clone(self):
        other = Tree()
        for i in range(len(self.nodes)):
            other.insert(self.nodes[i].value)
        return other
    
    """
    distance between 2 nodes
    """
    def getDist(self, n1, n2):
        if (self.updateFlag == True):
            self.updateDistances()
        if (n1.distances):
            return n1.distances[n1.find(n2.value)]
        else:
            graphN1 = self.find(n1.value)
            return graphN1.distances[graphN1.find(n2.value)]
#        else:#lazy hacking
#            dist_dict = gmaps.distance_matrix(self.nodes[i].value, self.nodes[j].value)
#            return dist_dict["rows"][0]["elements"][0]["distance"]["value"]
    
    """
    gives a deep copy of nodes references in given path p1
    """
    def copyPath(self, p1 = []):
        out = []
        for i in range(len(p1)):
            out.append(p1[i])
        return out
    
    """
    prints the given path of nodes
    """
    def printPath(self, path):
        for i in range(len(path)-1):
            print(path[i].value + "\n|\nV")
        print(path[len(path)-1].value + "\n")
    
    """
    needs nodes in path to be ordered
    returns total path distance given a path = array of nodes that are 
     connected through children
    """
    def getPathDistance(self, path):
        total = 0
        if (len(path) > 0):
            for i in range(len(path)-1):
                total += self.getDist(path[i], path[i+1])
        return total
    
    """
    uses treeRec to make a recursive tree using the graph
    """
    def toRecTree(self, node):
        if (node != None):
            tree_root = Node(node.value)
            if (not self.nodes[0].distances):
                self.updateDistances() # ensure values are stored
            for i in range(len(self.nodes)):
                if (self.nodes[i].value == tree_root.value):
                    continue
                tree_root.addChild(Node(self.nodes[i].value))
                #tree_root.distances.append(node.distances[node.find(self.nodes[i].value)])
                
            return self.treeRec(tree_root)
        return None
        
    def treeRec(self, node):
        if (len(node.children) > 1):#recursion end condition
            for child in node.children:
                #graphNode = self.find(child.value) # find value in self.nodes array
                for i in range(len(node.children)):
                    if (node.children[i] == child):
                        continue
                    child.addChild(Node(node.children[i].value))
                    #child.distances.append(graphNode.distances[graphNode.find(node.children[i].value)])
                self.treeRec(child)
        return node
            
            
    
    """
    DepthFirst Search: (Task 2)
    node is the starting point
    requires the tree to be connected as in all nodes should connected with
     a children link somewhere
    This can be optimised to STORE and use the shortest distance, the 
     corresponding best path and node count but not in scope of practical
    """
    def DepthFirstSearch(self, start):
        path = self.copyPath(self.nodes)
        shortSum = 0
        for i in range(len(path)-1):
            shortSum += self.getDist(path[i], path[i+1])
        
        shortSum += self.getDist(path[len(path)-1], start)
        self.DFSShortest = shortSum
        path.append(start)
        self.DFSPath = self.copyPath(path)
        #^ Just to set a reference to compare against and determine shortest route
        count = self.DFS(start, 0, [])
        print("Best DFS path: ")
        self.printPath(self.DFSPath)
        print("Shortest DFS Distance is " + str(self.DFSShortest)+ "m")
        print("DFS Path distance for checking: " + str(self.getPathDistance(self.DFSPath)) + "m")
        print("Total nodes visited(DFS): " + str(count))
        
    """
    start is the starting node
    total is the running total summed as path is traversed
    path is the accumulated path so far
    """
    #DFS works
    def DFS(self, start, total, path= []):
        if (len(path) == 0):
            rest = [i for i in start.children]
            #this can be the only possibility
            path.append(start)
        else:
            rest = [i for i in path[len(path)-1].children if i not in path]
            #children of last node in path that are not already in path
        if (len(rest) == 0):
            return 0
        currSum = 0
        if (len(rest) == 1): # just using the problem and hacking it for the solution
            curr = path[len(path)-1]
            currSum += self.getDist(curr, rest[0])
            if (currSum + total < self.DFSShortest):
                currSum += self.getDist(rest[0], start) #using the problem specs to my advantage here
                if (currSum + total < self.DFSShortest):
                    self.DFSShortest = currSum + total 
                    self.DFSPath = self.copyPath(path)
                    self.DFSPath.extend([rest[0], start])
                    #uncomment following two lines to see how best path is made
                    #print("current shortest = " + str(self.DFSShortest))
                    #self.printPath(self.DFSPath + "\n") 
                #return 2 #only distance from last to start checked. start is not processed
            return 0
        count  = 0
        for i in range(len(rest)):
            #remember to delete path elements in higher levels
            currSum = total + self.getDist(path[len(path)-1], rest[i])
            if (currSum < self.DFSShortest):
                path.append(rest[i])            
                count += self.DFS(start, currSum, path) +1
                path.remove(rest[i])
            currSum = 0
        return count
    
    """
    BreadthFirst Search: (Task 2)
    node is the starting point
    requires the tree to be connected as in all nodes should connected with
     a children link somewhere
    This can be optimised to STORE and use the shortest distance, the 
     corresponding best path and node count but not in scope of practical
    """
    def BreadthFirstSearch(self, start):
        path = self.copyPath(self.nodes)
        shortSum = 0
        for i in range(len(path)-1):
            shortSum += self.getDist(path[i], path[i+1])
        
        shortSum += self.getDist(path[len(path)-1], start)
        self.BFSShortest = shortSum
        path.append(start)
        self.BFSPath = path
        #^ Just to set a reference to compare against and determine shortest route
        BFSstart = self.toRecTree(start)
        count = self.BFS(BFSstart)
        print("Shortest BFS Distance is " + str(self.BFSShortest)+ "m")
        print("Total nodes visited(BFS): " + str(count))
    
              
    #adapted from asnwer given by amit at https://stackoverflow.com/questions/29141501/how-to-implement-bfs-algorithm-for-pacman   
    """
    begins from start and creates a queue to Bread first search and compare 
     accumulated route distance to previously recorded shortest distance
     and set new shortest distance if found
    """
    def BFS(self, start):
        unvisited = Queue()
        unvisited.put(start)
        count = 1
        pathDistances = dict()
        pathDistances[start] = 0 # stores current distance in path for a node
        
        while(not unvisited.empty()):
            curr = unvisited.get()
            #distance = pathDistances[]
            currSum = pathDistances[curr]
            rest = [i for i in curr.children]
            if (currSum < self.BFSShortest):
                for i in range(len(rest)):
                    if (i == 0):
                        currSum += self.getDist(curr, rest[i])
                    else:
                        currSum += self.getDist(rest[i-1], rest[i] )
                    pathDistances[rest[i]] = pathDistances[curr] + self.getDist(curr, rest[i])
                    
                    count += 1                
                    if (currSum < self.BFSShortest):
                        if (i == len(rest)-1 and currSum + self.getDist(rest[i], start) < self.BFSShortest):
                            self.BFSShortest = currSum + self.getDist(rest[i], start)
                    unvisited.put(rest[i])
        return count
    
tree = Tree()
tree.insert("University of Pretoria, Pretoria")
tree.insert("Denel Dynamics, Nellmapius Drive, Centurion")
tree.insert("CSIR, Meiring Naude Road, Pretoria")
tree.insert("Air Force Base Waterkloof, Centurion")
tree.insert("Armscor, Delmas Road, Pretoria")
tree.updateDistances()

tree.DepthFirstSearch(tree.root)
print()
tree.BreadthFirstSearch(tree.root)

