t1 = int(input())
t2 = int(input())
tG = 0
tP = 0

if(t1>t2):
    tG = t1
    tP = t2
else:
    tG = t2
    tP = t1

if(float((tG/tP)-1) < 0.15):
    print('Compara saltos')
    print('éxcuta cm menor saltos')
else:
    print(tP)