import sys, time, socket, threading
from Vars import *
import pickle
from RtpPacket import RtpPacket


"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.0.0.1', Port_Monitor))
data = ['10.0.0.10']#, sys.argv[1], sys.argv[2]]
sdata = pickle.dumps(data)
s.send(sdata)
time.sleep(1)
s.close()#"""

def forwarded(x,th):
    while True:
        if(dispara.isSet()):
            print(f"Dispara {th['bind']}")
            s.sendto(packet, x)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((sys.argv[1],Port_Stream))
""""
while True:
    packet, addr = s.recvfrom(BUFF_SIZE)
    s.sendto(packet,(sys.argv[2], Port_Stream))
#"""
global target
global packet

packet = None
target = {}
global dispara

dispara = threading.Event()
while True:
    packet, addr = s.recvfrom(BUFF_SIZE)
    dispara.clear()
    try:
        packetDecoded = packet.decode()
        if(packetDecoded == 'stepup'):
            print('recebi')
            #target.append(addr)
            target[addr[0]] = {}
            s.sendto(packet,('10.0.0.10',Port_Stream))
            target[addr[0]]['bind'] = addr
            target[addr[0]]['thread'] = threading.Thread(target=forwarded, args=(addr,target[addr[0]],))
            target[addr[0]]['thread'].start()
            print(target)
        #pass
    #"""
    except:
        dispara.set()
        pass
    #"""

    """
        for x in target:
            s.sendto(packet,x)
            #"""
