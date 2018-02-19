# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 17:39:03 2018

@author: Vishal
"""
from __future__ import print_function

#Perhaps having a graph-like structure would be more efficient here.
#The implementation would still involve children but only as links through
# an array of nodes that have a children array each with the other location
# titles and not actual node objects. But I shall be taking the class
# explained approach here.
class node(object): #needed for new style class
    #class will only hold a value which will be title and children nodes
    def __init__(self, value):
        self.value = value 
        self.children = []
        
    def find(self, value):
        i = 0
        while (i != len(self.children) and self.children[i].value != value):
            i += 1
        return i
      
    #don't clutter the tree unnecessarily since there is no delete method    
    def addChild(self, index, child):
#        for i in range(0, len(children)):
#            index = self.find(child.value)
#            if index == len(self.children):
#                self.children.append(child)
#            else:
        self.children.insert(index, child)
    
    #searches for value in children array and returns bool value for duplicate
    
            
        

class Tree(object):
    def __init__(self):
        self.root = None
        
#    #recursively builds the tree
#    #inefficient in long term but serves purpose
#    def insertRec(self, parent, children = []):
#        # for the last leaf in the tree
#        if (len(children) == 1):
#            parent.addChildren([node(children[0].value)])
#            return
#        #recursively add children and discard the parent
#        # node in the children list
#        if (len(children) > 0):
#            for i in range(0, len(children)):
#                temp = []
#                index = 0
#                while (len(temp) < len(children)-1):
#                    if (index == i):
#                        index += 1
#                    temp.append(node(children[index].value))
#                    index += 1
#                self.insertRec(children[i], temp)
        
#    def insertRec(self, parent, children = []):
#        if (len(children) > 0):
#            if (len(children) == 1):
#                parent.addChildren(children[0].value)
#            for i in range(0, len(children)):
#                temp = []
#                index = 0
#                while (len(temp) < len(children)-1):
#                    if (index == i):
#                        index += 1
#                    temp.append(children[index].value)
#                    index += 1
#                children[i].addChildren(temp)    
#                self.insertRec()
#        
#    def insert(self, value):
#        if (self.root == None):
#            self.root = node(value)
#            return
#        self.root.addChildren([node(value)])
#        self.insertRec(self.root, self.root.children)
        
    def insert(self, value):
        if (self.root == None):
            self.root = node(value)
            return
        self.root.addChild(len(self.root.children), node(value))
        #print(self.root.children[0])
        self.insertRec(self.root)
        
    def insertRec(self, parent):
#            if (len(parent.children) == 1):
#                parent.addChild(node(parent.children[0].value))
#                return
            #ssubTrees = []
#            if (len(parent.children) == 2):
#                parent.children[0].addChild(node(parent.children[1].value))
#                parent.children[1].addChild(node(parent.children[0].value))
#                return
            for i in range(0, len(parent.children)):
#                if (len(children) == 1):
#                    parent.addChild(children[0].value)
#                temp = []
                index = 0
                count = 0
                while(index < len(parent.children)):
                    if (index == i):
                        index += 1
                    if (index < len(parent.children)):
                        parent.children[i].addChild(count, node(parent.children[index].value))
#                    parent.addChild(parent.children[i])
                    index += 1
                    count += 1
                if (len(parent.children) > 2):
                    self.insertRec(parent.children[i])
#            for i in range(0, len(children)):
#                self.insertRec(children[i], subTrees[i])
            
    
    def printRec(self, node):
        for i in range(0, len(node.children)):
            print(node.children[i].value)
        
        if (len(node.children) > 1):
            print()
            for i in range (0, len(node.children)):
                self.printRec(node.children[i])
                print()

    #prints the levels of a search tree 
    def printTree(self):
        print(self.root.value + '\n')
        self.printRec(self.root)
    
    #just a test function
    def inspect(self):
        out = ""
        for i in range(0, len(self.root.children)):
            out += self.root.children[i].value + '\n'
        out += '\n'
        print(out)
        
        out = ""
        for i in range(0, len(self.root.children[0].children)):
            out += self.root.children[0].children[i].value + '\n'
        out += '\n'
        print(out)
        
        out = ""
        for i in range(0, len(self.root.children[0].children[0].children)):
            out += self.root.children[0].children[0].children[i].value + '\n'
        out += '\n'
        print(out)
    def getLeaf(self):
        print(self.root.children[0].children[0].children[0].children[0].value)
    
    
        
tree = Tree()
tree.insert("University of Pretoria, Pretoria")
tree.insert("CSIR, Meiring Naude Road, Pretoria")
tree.insert("Armscor, Delmas Road, Pretoria")
#tree.printTree()
#tree.getLeaf()
tree.insert("Denel Dynamics, Nellmapius Drive, Centurion")
#tree.inspect()
tree.printTree()
#tree.getLeaf()
tree.insert("Air Force Base Waterkloof, Centurion")
#tree.printTree()
#tree.inspect()
#tree.getLeaf()