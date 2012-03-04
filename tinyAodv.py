# Project: tinyAodv
# I just want to simulate the characteristics of AODV,
# one of the route protocl in MANET. this should be interesting.
# author: cipher
# create date: 2012-3-1
# Main_version: 0.1


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

    packetQueue = {}
    staticsQueue = {}
    routeTable = {}
    def __init__(self):
        pass
    def send(self):
        pass
    def receive(self):
        pass

class AODV(RouteProtocl):
    
    addr = 0
    broadcast_id = 0
    sequenceNo = 0;
   
    rreqQueue = []
    rrepQueue = []

    
    
    def __init__(self, addr):
        self.addr = addr
        self.packetQueue = dict( zip( ('rcv', 'snd'), ([],[]) ) )
        self.staticsQueue = dict( zip( ('rcvd','sndd'),
                                       (dict(zip(('HELLO','RREQ','RREP','RERR','DATA'), 
                                             ([],[],[],[],[])))
                                        ,dict(zip(('HELLO','RREQ','RREP','REER','DATA'), 
                                              ([],[],[],[],[]) ) ) )))
        self.rreqQueue = list()
        self.rrepQueue = list()
        self.routeTable = dict()
        #self.packetQueue['snd'].append([self.addr, 'broadcast', ['HELLO', self.addr,100] ])
        #self.packetQueue['snd'].append([self.addr, 'broadcast', ['RREQ', 11, 99, 11, 20, 99, 5] ] )
    def timer(self):
        pass
                    
                    
    def generatePacket(self, packet):
        self.packetQueue['snd'].append(packet)
        
    def send(self):
        packet = self.processSendPacket()
        return packet

    def receive(self, packet):
        if  packet != False and packet[0] != self.addr:
            self.packetQueue['rcv'].append(packet)
        self.processReceivedPacket()

    # HELLO packet:< my_ip, 'broadcast', ['HELLO', my_ip, seq_#] >
    # RREQ  packet:< my_ip, 'broadcast', ['RREQ', source_addr, source_sequence#, broadcast_id, dest_addr, dest_sequence#, hop_cnt] >
    # RREP  packet:< my_ip, nxt_ip, ['RREP', s_addr, d_addr, d_seq#, hop_cnt, lifetime]>
    
    #['HELLO', my_ip, seq_#]
    #['RREQ', source_addr, source_sequence#, broadcast_id, dest_addr, dest_sequence#, hop_cnt]
    #['RREP', s_addr, d_addr, d_seq#, hop_cnt, lifetime]
    #[source_addr, source_sequence#, broadcast_id, dest_addr ] rreqQueue

    
    def helloPktSend(self, packet):
        pass
    def rreqPktSend(self, packet):
        pass
            
    def rrepPktSend(self, packet):
        pass
    def rerrPktSend(self, packet):
        pass
    def dataPtkSend(self, packet):
        pass 
    def processSendPacket(self):
        sendPacketDispatcher = {'HELLO':self.helloPktSend, 'RREQ':self.rreqPktSend, 'RREP':self.rrepPktSend,
                                'RERR':self.rerrPktSend, 'DATA':self.dataPtkSend}
        try:
            packet = self.packetQueue['snd'].pop(0)
            sendPacketDispatcher[packet[2][0]](packet)
            self.staticsQueue['sndd'][packet[2][0]].append(packet[2][1:])
            return packet
        except:
            return False

    def helloPktReceived(self, packet):
        print 'node',self.addr,'received a HELLO from', packet[0]
        helloPacket = packet[2]
        self.routeTable[helloPacket[1]] = dict(zip( ('ntHop', 'numOfHops', 'dstSeqNo', 'actvNgbrs', 'expirTime'),
                                                    (helloPacket[1], 1, helloPacket[2], [], 3 )))
        return True

    def rreqPktReceived(self, packet):

        # if the packet has already been recorded in rreqQueue, just return
        for t, entry in self.rreqQueue:
            if entry[1] == packet[2][1] and  entry[3] == packet[2][3]:
                return False

        print 'node',self.addr,'received a RREQ from',packet[0], 'which is', packet[2][1], '->',packet[2][4]
        
        # if the packet is for me
        if packet[2][4] == self.addr:
            self.packetQueue['snd'].append( [self.addr, packet[0],
                                             ['RREP', packet[2][1], packet[2][4], self.sequenceNo, 1, 'lifeTime']] )
            return True

        
        # updata the routeTable
        self.routeTable[packet[2][1]] = dict(zip( ('ntHop', 'numOfHops', 'dstSeqNo', 'actvNgbrs', 'expirTime'),
                                                  (packet[0], packet[2][6], packet[2][2], [], 3 )))
        try:
            # if there is a entry in route Table and dst_seq_no > packet's dst_seq_no
            if self.routeTable[packet[2][4]]['dstSeqNo'] > packet[2][5]:
                entry = self.routeTable[packet[2][4]]
                self.packetQueue['snd'].append( [self.addr, entry['ntHop'], 
                                                 ['RREP',packet[2][1], packet[2][4], entry['dstSeqNo'], entry['numOfHops'], 'lifeTime'] ] )
        except:
           self.rreqQueue.append( [0, packet[2]] )
           
           #broadcast_id + 1
           tmpPacket = packet[2][:]
           tmpPacket[6] += 1 
           self.packetQueue['snd'].append( [self.addr, 'broadcast',tmpPacket] )
        return True

    # HELLO packet:< my_ip, 'broadcast', ['HELLO', my_ip, seq_#] >
    # RREQ  packet:< my_ip, 'broadcast', ['RREQ', source_addr, source_sequence#, broadcast_id, dest_addr, dest_sequence#, hop_cnt] >
    # RREP  packet:< my_ip, nxt_ip, ['RREP', s_addr, d_addr, d_seq#, hop_cnt, lifetime]>
    
    #['HELLO', my_ip, seq_#]
    #['RREQ', source_addr, source_sequence#, broadcast_id, dest_addr, dest_sequence#, hop_cnt]
    #['RREP', s_addr, d_addr, d_seq#, hop_cnt, lifetime]
    #[source_addr, source_sequence#, broadcast_id, dest_addr ] rreqQueue
    def rrepPktReceived(self, packet):
        print 'node',self.addr,'received a RREP from',packet[0], 'which is', packet[2][1], '->',packet[2][2]

        # record the route entry from dst to me
        self.routeTable[packet[2][2]] =  dict(zip( ('ntHop', 'numOfHops', 'dstSeqNo', 'actvNgbrs', 'expirTime'),
                                                  (packet[0], packet[2][4], packet[2][3], [], 3 )))

        # TODO: delete the entry in the rreqQueue
        for index, entry in zip(xrange(sys.maxint), self.rreqQueue):
            if packet[2][1] == entry[1][1] and packet[2][2] == entry[1][4]:
                print '+--A successful Route Discorvery from', packet[2][1], 'to', packet[2][2]
                self.rreqQueue.pop(index)
                return True
        
        try:
            # if there is a route entry for the source
            # increase the hop_cnt then send
            entry = self.routeTable[packet[2][1]]
            tmpPacket = packet[2][:]
            tmpPacket[4] += 1
            self.packetQueue['snd'].append( [self.addr, entry['ntHop'], tmpPacket ] )
            print '+--Found a route to',entry['ntHop'], 'for RREP from', packet[2][1], 'to', packet[2][2]
            return True
        except:
            # else, just drop this RREP packet
            print '+--No route to', packet[2][1], 'RREP from', packet[2][1], 'to', packet[2][2], 'dropped'
            return False
            
    def rerrPtkReceived(self, packet):
        pass
    def dataPtkReceived(self, packet):
        pass

    def processReceivedPacket(self):
        recivedPacketDispatcher = {'HELLO':self.helloPktReceived, 'RREQ':self.rreqPktReceived, 'RREP':self.rrepPktReceived,
                    'RERR':self.rerrPtkReceived, 'DATA':self.dataPtkReceived }
        try:
            packet  = self.packetQueue['rcv'].pop(0)
            if packet[0] == self.addr:
                return
            if packet[1] != self.addr and packet[1] != 'broadcast':
                return

            if recivedPacketDispatcher[packet[2][0]](packet):
                self.staticsQueue['rcvd'][packet[2][0]].append(packet[2][1:])
        except:
            return




class Node:
    rPro = False
    mMod = False
    def __init__( self,rp, addr, mm, curPos, nxtPos, curSpeed,  *arg):
        self.rPro = rp(addr)
        self.mMod = mm(curPos, nxtPos, curSpeed, *arg)
        
    def move(self):
        self.mMod.move()

    def send(self):
        return self.rPro.send()
    def recive(self,packet):
        self.rPro.receive(packet)
        




nodes = [ Node(AODV,0,RandomWayPoint,[1,2],[4,5],1,1000,1000,10,0,20, 1 ), 
          Node(AODV,1,RandomWayPoint,[20,20], [23,24],1, 1000,1000,10,0,10, 1)]

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


# HELLO packet:< my_ip, 'broadcast', ['HELLO', my_ip, seq_#] >
# RREQ  packet:< my_ip, 'broadcast', ['RREQ', source_addr, source_sequence#, broadcast_id, dest_addr, dest_sequence#, hop_cnt] >
# RREP  packet:< my_ip, nxt_ip, ['RREP', s_addr, d_addr, d_seq#, hop_cnt, lifetime]>
nodes[0].rPro.generatePacket([0, 'broadcast',['HELLO',0,99 ]])
nodes[0].rPro.generatePacket([0,'broadcast',
                         ['RREQ',0,99,0,1,88,1 ]])
nodes[0].rPro.rreqQueue.append([0,['RREQ',0,99,0,1,88,1 ] ])

nodes[0].rPro.rreqQueue.append([0,['RREQ',0,99,0,99,88,1 ] ])
nodes[0].rPro.generatePacket([20,1,
                         ['RREP',0,99,77,2,0 ]])

for n in range(3):
    for netnode in nodes:
        i = netnode.rPro.addr
        packet = netnode.send()
        for node in nodes:
            if i != node.rPro.addr:
                node.recive(packet)

for netnode in nodes:
    print '+'*20
    print netnode.rPro.addr 
    print netnode.rPro.staticsQueue
    print 'routeTB',netnode.rPro.routeTable
    print 'packet', netnode.rPro.packetQueue
    print 'rreqQ', netnode.rPro.rreqQueue
    print 'rrepQ', netnode.rPro.rrepQueue
    print '+'*20
