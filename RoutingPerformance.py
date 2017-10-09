#By Ruchi Gupta, z3473389, and Michael Jefferies, z3418370

import sys
import time

#
#
# DEFINING SOME CLASSES
#
#

# A container for the information regarding a link between two nodes
class Link:
    def __init__(self,capacity,delay):
        # the amount of this link's capacity that is currently being used
        self.used = 0
        # the capacity of this link
        self.cap = capacity
        # the propogation delay of this link
        self.prop = delay

# A container for the information regarding a connection that we need to simulate
class Connection:
    def __init__(self, startTime, duration, fromNode, toNode):
        # When this connection should start
        self.time = startTime
        # How long the connection should last for
        self.length = duration
        # the index of the node this connection sends from
        self.fnode = fromNode
        # the index of the node this connection is sending information to
        self.tnode = toNode

#
#
# READING IN ARGUMENTS AND INITIALISING VARIABLES
#
#

# checking that there are at least 5 arguments. Not sure if this is needed, but I thought I would check anyway.
try: sys.argv[5]
except IndexError: print "ERROR: not enough arguments"

# network type - "CIRCUIT" or "PACKET"
type = sys.argv[1]

# network scheme - "SHP", "SDP", or "LLP"
scheme = sys.argv[2]

# Packet rate, in packets per second
rate = sys.argv[5]

# reading in the topology text file
with open(sys.argv[3]) as topFile:
    top = topFile.readlines()
# stripping out the newline characters
top = [x.strip() for x in top]

# reading in the workload text file
with open(sys.argv[4]) as workFile:
    work = workFile.readlines()
# stripping out the newline characters
work = [x.strip() for x in work]



# List of letters that are in the node graph ("A", "B", etc)
# Used to quickly check if a node already exists in the graph when initialising it, and to quickly work
# out the index of the require node in the list of nodes
nameList = []

# List of nodes in the graph
nodeList = []

# List of connections that need to be made
workList = []

#
#
# READING IN THE INFORMATION FROM THE TEXT FILES
#
#

#for line in top:
    #each line: [node 1] [node 2] [prop delay] [capacity]

    #parts = line.split()
    #n1 = parts[0]
    #n2 = parts[1]
    #delay = parts[2]
    #capacity = parts[3]

    #if

    #for each line check if the nodes exist.
        #if not, then create them
        #check if there's already a link between those two nodes
            #if not, add it


#for line in work:
    #print line
    #maybe store as list of some connection class?




#
#
# SIMULATING THE CONNECTIONS
#
#

# The time at which the simulation started
start = time.time()

# The list of currently simulated connections
# Add them as they start. pop them as they end.
connList = []

# since the connections are sorted by time by default
# I figure we can just look at the first in the work list, then pop them off as we start them
# If we do that, eventually that list will empty.
# Once both lists are empty, there's nothing left to do and we can print the results

# while len(workList)>0 and len(connList>0):
    #DO STUFF
