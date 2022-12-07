import time, sys

from datetime import datetime  

"""
target = ['10.0.0.1','10.0.0.56']

def verifIfthisTargetExist(addr):
        verif = False
        for x in target:
            if(x == addr):
                verif = True
        return verif

while True:
    a = input('insra:')
    if(not verifIfthisTargetExist(a)):
        target.append(a)
    else:
        print('ja existe')
    print(target)
    


a = time.time()


time.sleep(4)

b = time.time()

time.sleep(2)

c = time.time()




print(datetime.fromtimestamp(a))
print(datetime.fromtimestamp(b))
print(datetime.fromtimestamp(c))
"""

routesMonitor = {}
count2 = 1
route = ['10.0.1.1','10.0.2.1','10.0.5.1',5454.5]

for x in range(8):
    if(x == 1):
        routesMonitor[count2] = {'route': route[:-1], 'time': 1000}
    #routesMonitor[count2]['route'] = route[:-1]
    #routesMonitor[count2]['time'] = route[-1]
    else:
        routesMonitor[x] = {'route': ['10.0.'+str(x)+'.'+str(y) for y in range(3)], 'time': x*2.8455+0.001}

#print(routesMonitor)

#print(routesMonitor[3]['route'] == ['10.0.3.0', '10.0.3.1', '10.0.3.2'])
#routesMonitor = {}
#print('aguarde')
#time.sleep(0.5)
#print('pronto')
#print(routesMonitor)
#a = time.time()
#time.sleep(0.001)
#b = time.time()
#print(str((b-a)*1000))

routesMonitor[5]['time'] = 0.000000000101
routesMonitor[4]['time'] = 0.0000000001
routesMonitor[4] = {'route': ['10.2.3.5'], 'time': 0.0000000001}


"""
#print(routesMonitor[1])
tp = routesMonitor[0]['time']
p = routesMonitor[0]
G = None
tG = float(sys.maxsize)
select = None
for x in routesMonitor:    
    if(tp == routesMonitor[x]['time']):
        pass
    else:
        if(routesMonitor[x]['time']<tp):
            tG = tp
            G = p
            p = routesMonitor[x] 
            tp = routesMonitor[x]['time']
        else:
            G = routesMonitor[x]
            tG = routesMonitor[x]['time']

        if(float((tG/tp)-1) < 0.15):
            if(len(G['route']) < len(p['route'])):
                print('Grande')
                select = G
                tp = tG
                p = select
            else:
                print('pequeno')
                select = p
            print(select)
        else:
            select = p
            print(select['route'])
            #"""

#print(routesMonitor[4])
verif = False
route = ['10.2.3.5']
count2 = 7
if(count2 > 0):
    for i in range(count2):
        if(route == routesMonitor[i]['route']):
            verif = True
            break
print(verif)
#print(routesMonitor[4]['route'] == route)

for i in range(count2):
            if(route == routesMonitor[i]['route']):
                position = i
                break
print(i)
routesMonitor[i]['time'] = 10

print(routesMonitor)

