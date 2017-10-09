#By Ruchi Gupta, z3473389, and Michael Jefferies, z3418370

import sys

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
        self.cap = int(capacity)
        # the propogation delay of this link
        self.prop = float(delay)

# A container for the information regarding a connection that we need to simulate
class Connection:
    def __init__(self, startTime, duration, fromNode, toNode):
        # When this connection should start
        self.time = float(startTime)
        # How long the connection should last for
        self.length = float(duration)
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


# List of nodes in the graph. Key is the node's letter (e.g "A", "B").
# Value is a dictionary for the node's adjacency list
nodeDict = {}

#
#
# READING IN THE INFORMATION FROM THE TEXT FILES
#
#

for line in top:
    # each line: [node 1] [node 2] [prop delay] [capacity]

    parts = line.split()
    n1 = parts[0]
    n2 = parts[1]
    delay = parts[2]
    capacity = parts[3]
    
    # Add nodes to graph if they aren't alredy
    if n1 not in nodeDict:
        nodeDict[n1] = {}
    if n2 not in nodeDict:
        nodeDict[n2] = {}
    
    # Create instance of link class
    link = Link(capacity,delay)
    
    # if there's no link between the nodes, add the link
    if n2 not in nodeDict[n1]:
        nodeDict[n1][n2] = link
    if n1 not in nodeDict[n2]:
        nodeDict[n2][n1] = link


# List of connections that need to be made
workList = []


for line in work:
    # each line: [start time] [from node] [to node] [duration]
    
    parts = line.split()
    begins = parts[0]
    n1 = parts[1]
    n2 = parts[2]
    duration = parts[3]
    
    # make sure the origin and destination nodes are in graph
    if n1 not in nodeDict:
        nodeDict[n1] = {}
    if n2 not in nodeDict:
        nodeDict[n2] = {}
    
    # making an instance of the connection class
    connection = Connection(begins, duration, n1, n2)
    
    # add connection to list of connections we need to simulate
    workList.append(connection)


#
# TEST PRINT LOOP TO CHECK NODE GRAPH INITIALISED CORRECTLY. SPOILER: IT DID.
#

#for item in nodeDict:
    #print item
    #for i2 in nodeDict[item]:
        #print "link: "+i2

#
# SAME THING FOR WORK LIST
#
#for item in workList:
    #print item.fnode






#
#
# SIMULATING THE CONNECTIONS
#
#

# The list of currently simulated connections
# Add them as they start. pop them as they end.
connList = []

# since the connections are sorted by time by default
# I figure we can just look at the first in the work list, then pop them off as we start them
# If we do that, eventually that list will empty.
# Once both lists are empty, there's nothing left to do and we can print the results

while len(workList)>0 or len(connList)>0:
    print "connection made at: "+str(workList[0].time)
    workList.pop(0)
print "done"
