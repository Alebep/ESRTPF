from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import socket, threading, sys, traceback, os

from RtpPacket import RtpPacket

from Vars import *

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class ClienteGUI:
	
	# Initiation..
	def __init__(self, master, addr, port):
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.handler)
		self.createWidgets()
		self.addr = addr
		self.port = int(port)
		self.rtspSeq = 0
		self.sessionId = 0
		self.requestSent = -1
		self.teardownAcked = 0
		self.frameNbr = 0
		
	def createWidgets(self):
		"""Build GUI."""
		# Create Setup button
		self.setup = Button(self.master, width=20, padx=3, pady=3)
		self.setup["text"] = "Setup"
		self.setup["command"] = self.setupMovie
		self.setup.grid(row=1, column=0, padx=2, pady=2)
		
		# Create Play button		
		self.start = Button(self.master, width=20, padx=3, pady=3)
		self.start["text"] = "Play"
		self.start["command"] = self.playMovie
		self.start.grid(row=1, column=1, padx=2, pady=2)
		
		# Create Pause button			
		self.pause = Button(self.master, width=20, padx=3, pady=3)
		self.pause["text"] = "Pause"
		self.pause["command"] = self.pauseMovie
		self.pause.grid(row=1, column=2, padx=2, pady=2)
		
		# Create Teardown button
		self.teardown = Button(self.master, width=20, padx=3, pady=3)
		self.teardown["text"] = "Teardown"
		self.teardown["command"] =  self.exitClient
		self.teardown.grid(row=1, column=3, padx=2, pady=2)
		
		# Create a label to display the movie
		self.label = Label(self.master, height=19)
		self.label.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=5, pady=5) 
	
	def setupMovie(self):
		"""Setup button handler."""
		#print("Not implemented...")
		self.openRtpPort()
		#self.playMovie()
	
	def exitClient(self):
		"""Teardown button handler."""
		self.master.destroy() # Close the gui window
		os.remove(CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT) # Delete the cache image from video

	def pauseMovie(self):
		"""Pause button handler."""
		#print("Not implemented...")
		self.rtpSocket.sendto((str('pause')).encode(), (self.addr,self.port))
	
	def playMovie(self):
		"""Play button handler."""
		# Create a new thread to listen for RTP packets
		self.frameNbr = 0
		threading.Thread(target=self.listenRtp).start()
		self.playEvent = threading.Event()
		self.playEvent.clear()
	
	def listenRtp(self):		
		"""Listen for RTP packets."""
		num_jumps = 0
		rotas = ''
		jumps_not_received=True
		routes_not_received=True
		while True:
			#try:
			data = self.rtpSocket.recv(BUFF_SIZE)
			if data:
				try:
					data_decoded = data.decode('utf-8')
					print(data_decoded)
					# Se receber informação em vez do packet de vídeo:
					"""if data_decoded[0]=='S':
						if routes_not_received:
							rotas = data_decoded + ' -> ' + self.addr + ' (Cliente)\n'
							routes_not_received=False
					else:
						if jumps_not_received:
							num_jumps = int(data_decoded) + 1
							jumps_not_received = False"""
				except:
					rtpPacket = RtpPacket()
					rtpPacket.decode(data)
					
					currFrameNbr = rtpPacket.seqNum()
					print("Current Seq Num: " + str(currFrameNbr))
					print(' ')
					#print("Nº Saltos:",num_jumps)
					#print('Rotas:',rotas)
										
					if(currFrameNbr == 500):
						currFrameNbr = 0
						self.frameNbr = 0
					#"""
					if currFrameNbr > self.frameNbr: # Discard the late packet#"""
						self.frameNbr = currFrameNbr
					#"""
					try:
						self.updateMovie(self.writeFrame(rtpPacket.getPayload()))
					except:
						pass
			"""		

			except:
				# Stop listening upon requesting PAUSE or TEARDOWN
				if self.playEvent.isSet(): 
					break
				
				self.rtpSocket.shutdown(socket.SHUT_RDWR)
				self.rtpSocket.close()
				break
			#"""	
	
	def writeFrame(self, data):
		"""Write the received frame to a temp image file. Return the image file."""
		cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
		file = open(cachename, "wb")
		file.write(data)
		file.close()
		
		return cachename
	
	def updateMovie(self, imageFile):
		"""Update the image file as video frame in the GUI."""
		try:
			photo = ImageTk.PhotoImage(Image.open(imageFile))
			self.label.configure(image = photo, height=288) 
			self.label.image = photo
		except:
			pass	
	
	def openRtpPort(self):
		"""Open RTP socket binded to a specified port."""
		# Create a new datagram socket to receive RTP packets from the server
		self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# Set the timeout value of the socket to 0.5sec
		self.rtpSocket.settimeout(120)
		
		try:
		#	# Bind the socket to the address using the RTP port
		#	self.rtpSocket.bind((self.addr, self.port))
		#	print('\nBind \n')
			self.rtpSocket.sendto(str('stepup').encode(), (self.addr,self.port))
			print('pedido enviado com sucesso')
		except:
			tkinter.messageBox.showwarning('Unable to Bind', 'Unable to bind PORT=%d' %self.rtpPort)

	def handler(self):
		"""Handler on explicitly closing the GUI window."""
		self.pauseMovie()
		if tkinter.messageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.exitClient()
		else: # When the user presses cancel, resume playing.
			self.playMovie()
