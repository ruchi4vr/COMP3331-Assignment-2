#!/usr/bin/env python
# By Michael Jefferies, z3418370

import sys
import time

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

updates = False
runTime = time.time()
# Used to trigger debug print statements
if len(sys.argv)>6:
        updates = True

# List of nodes in the graph. Key is the node's letter (e.g "A", "B").
# Value is a dictionary for the node's adjacency list
nodeDict = {}

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

# A container for the information regarding a connection that we need to simulate. Recycling this class in my packet implementation
class Request:
    # A cache of the route.
    route = None
    def __init__(self, startTime, duration, fromNode, toNode):
        # When this connection should start
        self.time = float(startTime)
        # How long the connection should last for
        self.length = float(duration)
        # the index of the node this connection sends from
        self.fnode = fromNode
        # the index of the node this connection is sending information to
        self.tnode = toNode
        # the number of packets in this Connection
        self.packets = int(self.length*float(rate))

# class used in the search function
class SearchNode:
    def __init__(self, currentNode, newList, prevVal):
        # Current Node in the network
        self.node = currentNode
        # Path so far, NOT including current Node
        self.list = newList
        # Search value for this path (i.e. number of Hops, or total delay, or used capacity)
        self.val = 0
        if scheme == "SHP":
            # As the list doesn't include current node, length of that list = number of hops.
            self.val = prevVal+1
        elif scheme == "SDP":
            listLen = len(self.list)
            if listLen<=0:
                self.val = 0
            else:
                self.val = prevVal + nodeDict[self.list[listLen-1]][self.node].prop
        else: #LLP
            maxLoad = 0.0
            for node in self.list:
                nIndex = self.list.index(node)
                # If this is the last node in the path
                if nIndex==len(self.list)-1:
                    linkLoad = float(nodeDict[node][self.node].used)/float(nodeDict[node][self.node].cap)
                else:
                    link = nodeDict[node][self.list[nIndex+1]]
                    linkLoad = float(link.used)/float(link.cap)
                if linkLoad > maxLoad:
                    maxLoad = linkLoad
            self.val = maxLoad

class Route:
    def __init__(self, list, delay):
        self.path = list
        self.pdel = delay

#
#
# SEARCH FUNCTION. JUST ONE. FOR ALL THREE CASES. THREE IN ONE. THE HOLY TRINITY OF SEARCH FUNCTIONS, YOU COULD SAY.
#
#

# returns an instance of the Path class
def Search(fromNode, toNode):
    foundNodes = []
    expNodes = []

    # creating the initial SearchNode
    newSNode = SearchNode(fromNode, [], 0)

    foundNodes.append(newSNode)

    while len(foundNodes)>0:
        cNode = foundNodes.pop(0)
        for key in nodeDict[cNode.node].keys():
            nList = cNode.list[:]
            nList.append(cNode.node)

            newSNode = SearchNode(key, nList, cNode.val)

            otherNode = None

            # Check if a path to this Node has already been found
            for x in foundNodes:
                if x.node == newSNode.node:
                    otherNode = x

            if otherNode != None:
                if newSNode.val<otherNode.val:
                    foundNodes.remove(otherNode)
                    foundNodes.append(newSNode)
                    foundNodes.sort(key=lambda x: x.val)
            else:
                # Same thing, but for the expanded nodes.
                for x in expNodes:
                    if x.node == newSNode.node:
                        otherNode = x
                if otherNode != None: 
                    if newSNode.val<otherNode.val:
                        expNodes.remove(otherNode)
                        foundNodes.append(newSNode)
                        foundNodes.sort(key=lambda x: x.val)
                else:
                    foundNodes.append(newSNode)
                    foundNodes.sort(key=lambda x: x.val)
        if cNode.node == toNode:
            list = cNode.list
            list.append(cNode.node)
            if scheme == "SDP":
                toReturn = Route(list, cNode.val)
            else:
                delay = 0.0
                for x in range(1, len(list)):
                    delay += nodeDict[list[x-1]][list[x]].prop
                toReturn = Route(list, delay)
            return toReturn
        else:
            expNodes.append(cNode)
    print "returning null"
    return None

#
#
# HERE'S THE STATS WE NEED TO KEEP TRACK OF
#
#

numRequests = 0
successRequests = 0
numPackets = 0
successPackets = 0 # Failed packets and percentages can be derived
totalHops = 0 # Will divide by numRequests at the end to get average
totalDelay = 0 # Again, will divide to get average

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
    link = Link(capacity,float(delay))
    
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
    
    # making an instance of the request class
    request = Request(begins, duration, n1, n2)
    
    # If in packet mode, make the packets
    if type == "PACKET":
        numRequests += 1
        interval = 1.0/float(rate)
        cTime = request.time
        for x in range(0,request.packets):
            sTime = cTime + float(x)*interval
            packet = Request(sTime, 1, request.fnode, request.tnode)
            workList.append(packet)
    else:
        # add connection to list of connections we need to simulate
        workList.append(request)

workList.sort(key=lambda x:x.time) # sorting worklist for good measure


# Updating stats for number of requests. the else scenario is handle above.
if type == "CIRCUIT":
    numRequests = len(workList)
else:
    numPackets = len(workList)


#
#
# SIMULATING THE CONNECTIONS
#
#

if type == "CIRCUIT":
    # List of connections currently beings simulated
    openConns = []
    while len(workList)>0 or len(openConns)>0:

        if updates and time.time()-runTime>=12.0:
            runTime = time.time()
            if len(openConns)>0:
                nTime = openConns[0].time
            else:
                nTime = workList[0].time
            print "Currently at simulation time: "+str(nTime)
            print str(len(workList))+" of "+str(numRequests)+" requests remaining"


        if len(workList)>0 and (len(openConns)<=0 or workList[0].time < openConns[0].time):
            current = workList.pop(0)
            numPackets += current.packets # Updating statistics concerning number of packets

            route = Search(current.fnode, current.tnode)

            # Checking if the path has the available capacity for this connection
            free = True
            for x in range(1,len(route.path)):
                link = nodeDict[route.path[x-1]][route.path[x]]
                if link.used >= link.cap:
                    free = False
                    break
            if free:
                # Changing the time field to be the time that this connection closes, so openConns sorts correctly
                current.time += current.length
                # caching the path
                current.route = route

                openConns.append(current)
                openConns.sort(key=lambda x: x.time)

                # Updating the currently used capacity along the path
                for x in range(1,len(route.path)):
                    nodeDict[route.path[x-1]][route.path[x]].used+=1
            elif updates:
                print "BLOCKET: "+str(route.path)

        else:
            current = openConns.pop(0)

            # Updating statistics
            successPackets += current.packets
            successRequests += 1
            totalHops += len(current.route.path)-1
            totalDelay += current.route.pdel/1000.0 # dividing by 100 because the delay is in milliseconds

            # freeing up path capacity
            for x in range(1,len(current.route.path)):
                try:
                    nodeDict[current.route.path[x-1]][current.route.path[x]].used-=1
                except IndexError:
                    print "ERROR AT INDEX: "+str(x)

#
#
# PACKET SWITCHING HERE
#
#

else:
    # List of packets currently going through the network
    sent = []
    while len(workList)>0 or len(sent)>0:

        # Debug statements every 12 seconds
        if updates and time.time()-runTime>=12.0:
            runTime = time.time()
            if len(sent)>0:
                nTime = sent[0].time
            else:
                nTime = workList[0].time
            print "Currently at simulation time: "+str(nTime)
            print str(len(workList))+" of "+str(numPackets)+" packets remaining"



        if len(workList)>0 and (len(sent)<=0 or workList[0].time < sent[0].time):
            current = workList.pop(0)

            route = Search(current.fnode, current.tnode)

            # Checking if the path has the available capacity for this packet
            free = True
            delay = 0
            for x in range(1,len(route.path)):
                link = nodeDict[route.path[x-1]][route.path[x]]
                delay += link.prop
                if link.used >= link.cap:
                    if updates:
                        print "DROPPED due to link "+route.path[x-1]+"-"+route.path[x]
                    free = False
                    break
                
            if free:
                # print str(current.time)+"-----"+str(delay/1000.0)+"---->"+str(current.time+float(delay/1000.0))
                # Changing the time field to be the time that this connection closes, so 'sent' sorts correctly
                current.time += delay/1000.0
                # print str(current.time)
                current.length = delay/1000.0 # dividing by 100 to convert milliseconds to seconds
                # caching the path
                current.route = route

                sent.append(current)
                sent.sort(key=lambda x: x.time)

                # Updating the currently used capacity along the path
                for x in range(1,len(route.path)):
                    link = nodeDict[route.path[x-1]][route.path[x]]
                    link.used+=1

                    # Debug print statements
                    #if updates:
                    #    perc = float(link.used)/float(link.cap)*100.0
                    #    if perc > 97:
                    #        print "path "+route.path[x-1]+"->"+route.path[x]+" at "+str(perc)+"%. Currently "+str(link.used)+" of "+str(link.cap)
                    #        print str(len(sent))+" active packets" 

        else:
            current = sent.pop(0)
            # print "popped at: "+str(current.time)
            # Updating statistics
            successPackets += 1
            totalHops += len(current.route.path)-1
            totalDelay += current.route.pdel/1000.0

            # freeing up path capacity
            for x in range(1,len(current.route.path)):
                link = nodeDict[current.route.path[x-1]][current.route.path[x]]

                # Debug print statements
                #if updates:
                #    perc = float(link.used)/float(link.cap)*100.0
                #    if perc > 97:
                #        print "path "+current.route.path[x-1]+"->"+current.route.path[x]+" freed up"
                #        print str(len(sent))+" active packets"
                try:
                   link.used-=1
                except IndexError:
                    print "ERROR AT INDEX: "+str(x)

#
#
# PRINTING OUT THE RESULTS
#
#

# Debug print statements
if updates:
    for x in nodeDict:
        for y in nodeDict[x]:
            if nodeDict[x][y].used>0:
                print "Link "+x+"-"+y+" is faulty"

# calculating derived statistics
try:
    sucPer = (float(successPackets)/float(numPackets))*100
except ZeroDivisionError:
    sucPer = 0
if type == "CIRCUIT":
    avHop = (float(totalHops)/float(successRequests))
    avProp = (float(totalDelay)/float(successRequests))
else:
    avHop = (float(totalHops)/float(successPackets))
    avProp = (float(totalDelay)/float(successPackets))

print "total number of virtual circuit requests: "+str(numRequests)
print "total number of packets: "+str(numPackets)
print "number of successfully routed packets: "+str(successPackets)
print "percentage of successfully routed packets: "+str(round(sucPer,2))
print "number of blocked packets: "+str(numPackets-successPackets)
print "percentage of blocked packets: "+str(round(float(100)-sucPer,2))
print "average number of hops per circuit: "+str(round(avHop,2))
print "average cumulative propagation delay per circuit: "+str(round(avProp,2))
