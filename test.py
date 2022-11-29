import sys, time, socket
from Vars import *
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.0.0.1', Port_Monitor))
data = ['10.0.8.5', sys.argv[1], sys.argv[2]]
sdata = pickle.dumps(data)
s.send(sdata)
time.sleep(1)
s.close()