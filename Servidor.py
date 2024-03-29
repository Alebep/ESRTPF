import sys, socket

from random import randint
import sys, traceback, threading, socket
import pickle

from VideoStream import VideoStream
from RtpPacket import RtpPacket
from time import time,sleep

import time as tempo

from Vars import *

class Servidor:	
	flagPause = False
	def sendRtp(self,nodeOverlay):
		"""Send RTP packets over UDP."""
		#frameNumber = 0
		while True:
			#for nodeOverlay in self.nodeOverlays:
			nodeOverlay['event'].wait(0.05)
			
			# Stop sending if request is PAUSE or TEARDOWN
			if nodeOverlay['event'].isSet():
				break
				
			data = nodeOverlay['videoStream'].nextFrame()
			if data:
				frameNumber = nodeOverlay['videoStream'].frameNbr()
				try:
					global address #= nodeOverlay['rtpAddr']
					global port #= int(nodeOverlay['rtpPort'])
					packet =  self.makeRtp(data, frameNumber)
					#envia o stream
					if(nodeOverlay['com'].isSet()):
						print('estou a mandar')
						nodeOverlay['rtpSocket'].sendto(packet,(address,port))
					if(frameNumber == 500):
						nodeOverlay['videoStream'] = VideoStream("movie.Mjpeg")
				except:
					print("Connection Error")
					print('-'*60)
					traceback.print_exc(file=sys.stdout)
					print('-'*60)
		# Close the RTP socket
		#nodeOverlay['rtpSocket'].close()
		print("All done!")
		nodeOverlay['event'].clear()

	def makeRtp(self, payload, frameNbr):
		"""RTP-packetize the video data."""
		version = 2
		padding = 0
		extension = 0
		cc = 0
		marker = 0
		pt = 26 # MJPEG type
		seqnum = frameNbr
		ssrc = 0
		
		rtpPacket = RtpPacket()
		
		rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)
		print("Encoding RTP Packet: " + str(seqnum))
		
		return rtpPacket.getPacket()

	
	def main(self,sk,nodeOverlay):
		try:
			# Get the media file name
			filename = "movie.Mjpeg"
			print("Using provided video file ->  " + filename)
			# videoStream
			nodeOverlay['videoStream'] = VideoStream(filename)
			# Create a new socket for RTP/UDP
			nodeOverlay["rtpSocket"] = sk
			nodeOverlay['worker']= threading.Thread(target=self.sendRtp, args=(nodeOverlay,))
			nodeOverlay['worker'].start()
		except:
			print("[Usage: Servidor.py <videofile>]\n")

def Boot(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, Port_Monitor))
	data = [sys.argv[1]]
	sdata = pickle.dumps(data)
	s.send(sdata)
	sleep(1)
	s.close()
 
def Monitor(ip):
	t = sys.argv[1]
	"""
	firts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	firts.connect((ip, Port_realMonitor))
	data = [t,time()]
	sdata = pickle.dumps(data)
	firts.send(sdata)
	print('enviou')
	sleep(0.01)
	firts.close()
	#"""
	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, Port_realMonitor))
		data = [t, tempo.time_ns()]#[t,time()]
		sdata = pickle.dumps(data)
		s.send(sdata)
		print('pacote de monitoramento enviado')
		sleep(0.0015)
		s.close()
		sleep(30)
  
# sys.argv[1] -> ip do servidor
#sys.argv[2] -> ip do no a frente do servidor

def main():
    # chamar o streaming fora do ciclo, e colocar uma flag que pega o endereco e define quando mandar
    serverW = Servidor()
    global port
    global address
    #Boot(sys.argv[2])
    threading.Thread(target=Monitor, args=(sys.argv[2],)).start()
	#serverW.
	# variavel compartilhada em threadsW
    nodeOverlay = {}
    nodeOverlay['event'] = threading.Event()
    nodeOverlay['com'] = threading.Event()
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((sys.argv[1],Port_Stream))#Port_Stream
    serverW.main(s, nodeOverlay)
    while True:
        try:
            print('A escuta')
            msg, addr = s.recvfrom(1024)
            print(f"Cliente {addr} conectado")
            #print('mensagem: {0}'.format(msg.decode()))
            #s.sendto(str(addr[1]).encode(), addr)
            if(msg.decode() == 'stepup'):
                print('chegou pedido')
                address = addr[0]
                port = addr[1]
                nodeOverlay['com'].set()
            elif(msg.decode() == 'stop'):
                nodeOverlay['event'].set()
            elif(msg.decode() == 'pause'):
                nodeOverlay['com'].clear()
            else:
                pass
        except:
            print('Ocorreu algum erro!')
            break
    s.close()

address : str
port : int

if __name__ == "__main__":
    main()    
