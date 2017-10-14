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

# packet
class Packet:
    def __init__(self,time,path,last):
        # The time at which this packet will reach the next node on its path (or be sent)
        self.time = time
        # the node that this packet is travelling from
        self.fromNode = null
        # Flags this as the last package in CIRCUIT communication
        self.isLast = last
        # A copy of the full path if this is the last packet in a circuit request. Used to free up capacity when done
        self.cachedPath = []
        if self.isLast:
            self.cachedPath = path[:]
        # The remaining nodes on its path
        self.path = path[:]
        # The node that the packet is travelling to
        self.node = self.path.pop(0)

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
# HERE'S THE STATS WE NEED TO KEEP TRACK OF
#
#

numRequests = len(workList)
numPackets = 0
successPackets = 0 # Failed packets and percentages can be derived
totalHops = 0 # Will divide by numRequests at the end to get average
totalDelay = 0 # Again, will divide to get average

#
#
# SIMULATING THE CONNECTIONS
#
#

# since the connections are sorted by time by default
# I figure we can just look at the first in the work list, then pop them off as we start them
# If we do that, eventually that list will empty.
# Once both lists are empty, there's nothing left to do and we can print the results

packList = []
# Variables from earlier are 'type', 'scheme', and 'rate'

while len(workList)>0 or len(packList)>0:
    if(len(packList)<=0 or workList[0].time>=packList[0].time):
        print "THIS IS WHERE WE CALL THE SEARCH FUNCTION AND CREATE PACKETS"

        # path = [INSERT SEARCH FUNCTION CALL HERE]
        path = ['A','B','C','D','E','F','G','H'] # Test path just to make sure everything else works

        # Updating statistics
        totalHops += len(path)-1
        for x in range(1,len(path)):
            totalDelay += nodeDict[path[x-1]][path[x]].prop
        # NEED TO CALCULATE TOTAL PACKETS

        circuitFree = True
        # if circuit check path availability now. Set above variable to false
        if type == "CIRCUIT":
            for x in range(1,len(path)):
                if(nodeDict[path[x-1]][path[x]].cap-nodeDict[path[x-1]][path[x]].used)<=0:
                    circuitFree = False
            if circuitFree:
                for y in range(1,len(path)):
                    nodeDict[path[y-1]][path[y]].used+=1

        

        # if circuitFree, create packets and add them to packlist. DON'T FORGET TO USE [:]
        # def __init__(self,time,path,last):


        workList.pop(0)
    else:
        print "MOVE PACKET TO NEXT NODE HERE"
        # check if at last node in path
        # if so, add to stats and remove. Don't forget to check circuit flag
        # check if next 


#
#
# PRINTING OUT THE RESULTS
#
#

# calculating derived statistics
try:
    sucPer = (float(successPackets)/float(numPackets))*100
except ZeroDivisionError:
    sucPer = 0
avHop = (float(totalHops)/float(numRequests))
avProp = (float(totalDelay)/float(numRequests))

print "total number of virtual circuit requests: "+str(numRequests)
print "total number of packets: "+str(numPackets)
print "number of successfully routed packets: "+str(successPackets)
print "percentage of successfully routed packets: "+str(sucPer)
print "number of blocked packets: "+str(numPackets-successPackets)
print "percentage of blocked packets: "+str(float(100)-sucPer)
print "average number of hops per circuit: "+str(avHop)
print "average cumulative propagation delay per circuit: "+str(avProp)

# EVERTHING AFTER HERE IS JUST A COMMENT



#List of Packets

#if next thing is start a new connect
    #search for path using A* with command line determined thing
    #create packet instances based on that
    #add those packets to packet list
    #add relevant statistics
    #pop connection from connection list
#else if next thing is a packet changing state
    #update packet, resort packet list

#when connection and packet lists are both empty, script is done




#TASKS

#nodeDict['A']['B'] instance of Link object from A to B


#FOR THE WEEKEND
#Above loop for creating and interacting with packets
#A* for SHP and SDP returns list of characters ["A", "C" etc']

#BY WEDNEDSAY, MAYBE COLLAB ON TUESDAY?
#LLP

#ON THURSDAY SCREENCAST


# NOTE TO SELF, if I edit nodeDict['A']['B'], does that also change nodeDict['B']['A'] - ANSWER: YES, it does.
