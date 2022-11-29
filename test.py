import sys, time, socket
from Vars import *
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.0.0.1', Port_Monitor))
data = [sys.argv[1]]
sdata = pickle.dumps(data)
time.sleep(1)
s.send(sdata)
time.sleep(1)
s.close()