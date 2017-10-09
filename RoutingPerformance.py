#By Ruchi Gupta, z3473389, and Michael Jefferies, z3418370

import sys
import time


#checking that there are at least 5 arguments. Not sure if this is needed, but I thought I would check anyway.
try: sys.argv[1]
except IndexError: print "ERROR: not enough arguments"

#network type - "CIRCUIT" or "PACKET"
#type = sys.argv[1]

#network scheme - "SHP", "SDP", or "LLP"
#scheme = sys.argv[2]

#Packet rate, in packets per second
#rate = sys.argv[5]

#reading in the topology text file
with open(sys.argv[3]) as topFile:
    top = topFile.readlines()
#stripping out the newline characters
top = [x.strip() for x in top]

#for line in top:
    #print line
    #each line: [node 1] [node 2] [prop delay] [capacity]

    #for each line check if the nodes exist.
        #if not, then create them
        #check if there's already a link between those two nodes
            #if not, add it
    

#reading in the workload text file
with open(sys.argv[4]) as workFile:
    work = workFile.readlines()
#stripping out the newline characters
work = [x.strip() for x in work]

#for line in work:
    #print line
    #maybe store as list of some connection class?
