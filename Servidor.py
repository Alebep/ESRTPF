import sys, socket

from random import randint
import sys, traceback, threading, socket

from VideoStream import VideoStream
from RtpPacket import RtpPacket

class Servidor:	

	def sendRtp(self,nodeOverlay):
		"""Send RTP packets over UDP."""
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
					address = nodeOverlay['rtpAddr']
					port = int(nodeOverlay['rtpPort'])
					packet =  self.makeRtp(data, frameNumber)
					nodeOverlay['rtpSocket'].sendto(packet,(address,port))
					# O nº de saltos é incrementado todas as vezes que o fluxo passa por um nó.
					init_num_jumps = '0' 
					nodeOverlay['rtpSocket'].sendto(bytes(init_num_jumps,'utf-8'),(address,port))
					# Rota começa vazia e vai sendo construída ao longo das ligações.
					rota_inicial = 'Servidor'
					nodeOverlay['rtpSocket'].sendto(bytes(rota_inicial,'utf-8'),(address,9999))
				except:
					print("Connection Error")
					print('-'*60)
					traceback.print_exc(file=sys.stdout)
					print('-'*60)
		# Close the RTP socket
		nodeOverlay['rtpSocket'].close()
		print("All done!")

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

	
	def main(self):
		try:
			# Get the media file name
			filename = "movie.Mjpeg"
			print("Using provided video file ->  " + filename)
			# Enviar para os próximos nós a stream de vídeo
        	# bem como informação acerca das rotas e do nº de saltos.
			#for i in range(1,len(sys.argv)):
			nodeOverlay = {}
			# videoStream
			nodeOverlay['videoStream'] = VideoStream(filename)
			# sockets
			nodeOverlay['rtpPort'] = 22751
			nodeOverlay['rtpAddr'] = sys.argv[1]
			print("Sending to Addr:" + nodeOverlay['rtpAddr'] + ":" + str(nodeOverlay['rtpPort']))
			# Create a new socket for RTP/UDP
			nodeOverlay["rtpSocket"] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			nodeOverlay['event'] = threading.Event()
			nodeOverlay['worker']= threading.Thread(target=self.sendRtp, args=(nodeOverlay,))
			nodeOverlay['worker'].start()
		except:
			print("[Usage: Servidor.py <videofile>]\n")
			
if __name__ == "__main__":
	(Servidor()).main()
