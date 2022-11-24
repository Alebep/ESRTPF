import sys, socket
import netifaces as ni
from tkinter import Tk
from ClienteGUI import ClienteGUI


if __name__ == "__main__":
	try:
		addr = sys.argv[1]
		port = 22751
	except:
		print("[Usage: Cliente.py]\n")	
	
	root = Tk()
	
	# Create a new client
	app = ClienteGUI(root, addr, port)
	app.master.title("Cliente Exemplo")	

	root.mainloop()
	
