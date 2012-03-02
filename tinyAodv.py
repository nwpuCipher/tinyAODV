# Project: tinyAodv
# I just want to simulate the characteristics of AODV,
# one of the route protocl in MANET. this should be interesting.
# author: cipher
# create date: 2012-3-1
# Main_version: 0.1
# change_log_1
# edit_by: cipher
# data: 2012-3-2
# sub_version: 0.1.1
#
# change_list:
# 1.reconstruct the MobileNode class, simplified all the code
# for reading
# 2.added new interfaces in RouteProtocl class, from which different
# route protocl class could be derived
# 3.changed a little bug in AODV class, which is caused by the
# defination of list in dict type. 
#
# problem:
# 1.a method for move model should be established, So the
# MobileNode will obey the SRP and will be decoupled.

# change_log_2
# edited_by： cipher
# data 2012-3-2
# sub_version: 0.1.1
#
# change_list:
# 1. in order to solove the problem.1, all the codes have been rewriten
# 2. added some comments for a good understand of some codes
# 3. added some method for processing packets in class AODV and the node
# could deliever HELLO packet now
#
# problem:
# 1. newly added codes must be constructed later


import math
import random
import sys
import pylab

# this func calc the distance between two point
def distance(p1,p2):
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

class MobileModel:
    # the param for the sence
    maxWidth = 10000
    maxHeight = 10000
    scale = 10
    minSpeed = 0
    maxSpeed = 20
    time = 1
    
    def __init__(self):
        pass
    
    def randomSpeed(self):
        return random.randint(self.minSpeed,self.maxSpeed)
    def randomWidth(self):
        return random.randint(-self.maxWidth/self.scale,self.maxWidth/self.scale)
    def randomHeight(self):
        return random.randint(-self.maxHeight/self.scale,self.maxHeight/self.scale)
    def move(self):
        pass
    
class RandomWayPoint(MobileModel):
    curPos = [0,0]
    nxtPos = [0,0]
    curSpeed = 0;
    def __init__(self, curPos, nxtPos, curSpeed, *arg):
        self.curPos = curPos
        self.nxtPos = nxtPos
        self.curSpeed = curSpeed
        
        self.maxWidth ,self.maxHeight, self.scale ,self.minSpeed, self.maxSpeed, self.time = arg
    def move(self):
        # if current speed = 0, we need to randomSpeed for this node
        if self.curSpeed == 0:
            self.setSpeed(self.randomSpeed())
            return
        # if the distance between current point and next point is below curSpeed
        # we need:
        # curPos = nxtPos
        # curSpeed = randomSpeed()
        # nxtPos = nextWayPoint -- w
        # else will calc the new current point with nextCurPoint()
        if( distance( self.curPos,self.nxtPos ) < self.curSpeed ):
            self.setCurPos(self.nxtPos)
            self.setSpeed(self.randomSpeed())
            self.setNxtPos(self.nextWayPoint())
        else:  
            self.setCurPos(self.nextCurPoint())
    
    def setCurPos(self,curPos):
        self.curPos = curPos
    def setNxtPos(self,nxtPos):
        self.nxtPos = nxtPos
    def setSpeed(self,curSpeed):
        self.curSpeed = curSpeed
    
    # divide the speed in x and y direction
    def divideSpeed(self):
        x = abs(self.curPos[0] - self.nxtPos[0])
        y = abs(self.curPos[1] - self.nxtPos[1])
        if x==0 and y==0:
            return 0, 0
        #l = math.sqrt(x**2 + y**2)
        l = distance([x,y], [0,0])
        return self.curSpeed * x / l, self.curSpeed * y/ l
    
    def nextWayPoint(self):
        x = self.curPos[0]+self.randomWidth()
        y = self.curPos[1]+self.randomHeight()
        while x < 0 or y < 0 or x > self.maxWidth or y > self.maxHeight:
            x = self.curPos[0]+self.randomWidth()
            y = self.curPos[1]+self.randomHeight()
        return x, y
    
    def nextCurPoint(self):
        vx, vy = self.divideSpeed()
        x, y = self.curPos
        if( self.nxtPos[0] >= self.curPos[0] ):
            x = x + vx * self.time
        else:
            x = x - vx * self.time
        if( self.nxtPos[1] >= self.curPos[1] ):
            y = y + vy * self.time
        else:
            y = y - vy * self.time
        return x, y



class RouteProtocl:
    neighbours = []
    packetQueue = {}
    staticsQueue = {}
    def __init__(self):
        pass
    def send(self):
        pass
    def receive(self):
        pass

class AODV(RouteProtocl):
    addr = 0

    
    def __init__(self):
        self.addr = random.randint(0,100)
        self.packetQueue = dict( zip( ('rcv', 'snd'), ([],[]) ) )
        self.staticsQueue = dict( zip( ('rcvd','sndd'),
                                       (dict(zip(('HELLO','RREQ','RREP','RERR','DATA'), 
                                             ([],[],[],[],[])))
                                        ,dict(zip(('HELLO','RREQ','RREP','REER','DATA'), 
                                              ([],[],[],[],[]) ) ) )))
        self.packetQueue['snd'].append(['HELLO', self.addr,100])

    def timer(self):
        pass
                    
                    

    def send(self):
        try:
            packet  =  self.packetQueue['snd'].pop(0)
            self.staticsQueue['sndd'][packet[0]].append(packet[1:0])
            return packet
        except:
            return False
    def receive(self, packet):
        if  packet != False and packet[1] != self.addr:
            self.packetQueue['rcv'].append(packet)
        self.processPacket()

    def HelloPkt(self, packet):
        self.neighbours.append(packet[1:])
        
    def RreqPkt(self, packet):
        pass
    def RrepPkt(self, packet):
        pass
    def RerrPtk(self, packet):
        pass
    def DataPtk(self, packet):
        pass




    def processPacket(self):
        dispatch = {'HELLO':self.HelloPkt, 'RREQ':self.RreqPkt, 'RREP':self.RrepPkt,
                    'RERR':self.RerrPtk, 'DATA':self.DataPtk}
        try:
            packet  = self.packetQueue['rcv'].pop(0)
            
        except:
            return

        dispatch[packet[0]](packet)
        self.staticsQueue['rcvd'][packet[0]].append(packet[1:])


class Node:
    rPro = False
    mMod = False
    def __init__( self,rp, mm, curPos, nxtPos, curSpeed,  *arg):
        self.rPro = rp()
        self.mMod = mm(curPos, nxtPos, curSpeed, *arg)
        
    def move(self):
        self.mMod.move()

    def send(self):
        return self.rPro.send()
    def recive(self,packet):
        self.rPro.receive(packet)
        




nodes = [ Node(AODV,RandomWayPoint,[1,2],[4,5],1,1000,1000,10,0,20, 1 ), 
          Node(AODV,RandomWayPoint,[20,20], [23,24],1, 1000,1000,10,0,10, 1) ]

arrx = [[],[]]
arry = [[],[]]

for i in range(2000):
    for index, node in zip( xrange(sys.maxint),nodes):
        node.move()
        pos = node.mMod.curPos
        arrx[index].append(pos[0])
        arry[index].append(pos[1])

#pylab.plot( arrx[0], arry[0], arrx[1], arry[1] )
#pylab.figtext(0.35,0.05,'node mobile modle')
#pylab.show()

for netnode in nodes:
    packet = netnode.send()
    for node in nodes:
        node.recive(packet)

for netnode in nodes:
    print netnode.rPro.addr, netnode.rPro.staticsQueue
    print netnode.rPro.neighbours
