import socket, tkinter, sys, pickle, threading, os
import netifaces as ni
from RtpPacket import RtpPacket
from time import time, sleep
import time as tm
from Vars import *

class Monitor:
    def __init__(self, sk):
       self.tcpSocket = sk#socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.timeSend = None
       self.timeRouteSelect = 0
       self.__oneTime = True
       #self.rotas = rotas
    
    def selectBestRoute(self):
        global routesMonitor
        global rotaSelect
        # inicializar o tempo, para comparacao
        tp = routesMonitor[0]['time']
        # rota do menor tempo
        p = routesMonitor[0]
        # rota do maior tempo
        G = None
        # inicializar maior tempo
        tG = float(sys.maxsize)
        # variavel que vai guardar a rota selecionada, inicializa com a rota inicial do tempo inicial
        select = p
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
                        select = G
                        tp = tG
                        p = select
                    else:
                        select = p
                    print(select)
                else:
                    select = p
                    print(select['route'])
                    #"""
        if(select['route'] == rotaSelect):
            pass
        else:
            rotaSelect = select['route']
    
    def thisRoutExists(self, route):
        global routesMonitor
        global count2
        verif = False
        if(count2 > 0):
            for i in range(count2):
                if(len(route[:-1]) == 1):
                    if([route[0]] == routesMonitor[i]['route']):
                        verif = True
                        break
                else:
                    if(route[:-1] == routesMonitor[i]['route']):
                        verif = True
                        break
        return verif

    def position(self, route):
        position = None
        for i in range(count2):
            if(route[:-1] == routesMonitor[i]['route']):
                position = i
                break
        return position
    
    def Add(self, route, time):
        global count2
        global predEmitter
        global routesMonitor
        global rotaSelect
        if(not self.thisRoutExists(route)):
            routesMonitor[count2] = {'route': route[:-1], 'time': time}
            count2 += 1
        else:
            pos = self.position(route)
            #try:
            routesMonitor[pos]['time'] = time
            #except:
            #    pass
            #"""
        if(count2 > 1):
            self.selectBestRoute()
            print(f"rota selecionada {rotaSelect}")
            if(self.__oneTime):
                predEmitter = rotaSelect[-1]
                self.__oneTime = False
            self.viewRouteTable(routesMonitor,rotaSelect)
            
    def __receviAndSend(self, conn):
        global myIP
        global neighbors
        packetList = conn.recv(BUFF_SIZE)
        print('recebeu monitoramento')
        #self.timeSend = tm.time()
        self.timeSend = tm.time_ns()
        if packetList:
            RouteFromAnte = pickle.loads(packetList)
            if( type(RouteFromAnte)  == type(list())):
                #tempo ate esse no em milisegundos
                time = (self.timeSend - RouteFromAnte[-1])/1000000
                self.Add(RouteFromAnte, time)
                #RouteFromAnte[-1] representa o tempo com origem no servidor
                data = RouteFromAnte[:-1] + [myIP, RouteFromAnte[-1]]
                sdata = pickle.dumps(data)
                for x in neighbors:
                    if(not (x in RouteFromAnte[:-1])):
                        print(x)
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((x,Port_realMonitor))
                        #time.sleep(1)
                        s.send(sdata)
                        sleep(0.001)
                        s.close()#"""
        
    def main(self):
        sleep(1)
        print('Monitoramento Ativado')
        while True:
            self.tcpSocket.listen(5)
            conn, addr = self.tcpSocket.accept()
            threading.Thread(target=self.__receviAndSend, args=(conn,)).start()
    
    def viewRouteTable(self,routes,selctRoute):
        tamTime = 25
        tamRoute = 90
        tamJump = 5
        #_ = os.system('clear') #or None
        print('-'*(7+tamRoute+tamTime+tamJump))
        print('|selct |'+' '*43+'route'+' '*43+'|       time'+' '*8+'  |'+'jump|')
        print('-'*(7+tamRoute+tamTime+tamJump))
        l = ''
        for x in routes:
            if(selctRoute == routes[x]['route']):
                l = '*'
            else:
                l = ''
            tam = len(list(str(routes[x]['route'])))
            tam2 = len(list(str(routes[x]['time'])))
            valorJump = len(routes[x]['route'])-1
            print('|'+str(l)+' '*(6-len(str(l)))+'|'+str(routes[x]['route'])+' '*((tamRoute+1)-tam)+'|'+str(routes[x]['time'])+' '*(21-tam2)+'|'+str(valorJump)+' '*3+'|')
            print('-'*(7+tamRoute+tamTime+tamJump))
        
    @staticmethod
    def selectBestRouteByJump(tableRoute):
        min_length = sys.maxsize
        select_route = None
        for x in tableRoute:
            if(len(tableRoute[x]) < int(min_length)):
                min_length = len(routers[x])
                select_route = x
        return tableRoute[select_route]
                


class Stream:
    def __init__(self, sk):
        # se target tem elementos e True, se nao e false
        self.active = False
        self.udpsocket = sk#socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#sk
    
    def activeOrNo(self):
        global target
        if(len(target) > 0):
            self.active = True
        else:
            self.active = False
    
    def forwardingStream(self, packet):
        global target
        self.activeOrNo()
        if(self.active):
            for x in target:
                self.udpsocket.sendto(packet,x)
    
    def sentToServer(self, packet):
        self.udpsocket.sendto(packet,(rotaSelect[-1],Port_Stream))
        
    def verifIfthisTargetExist(self,addr):
        verif = False
        for x in target:
            if(x == addr):
                verif = True
        return verif
    
    def refresEmiiterStream(self):
        global predEmitter
        global rotaSelect
        global target
        global changeRoute
        while True:
            try:
                #Essa condicao é s para garantir que o target nao envia pacotes para orgem caso venha a ser selctroute
                if(not (rotaSelect[-1] in target)):
                    if(predEmitter != rotaSelect[-1]):
                        if(len(target)>0):
                            self.udpsocket.sendto(str('pause').encode(),(predEmitter, Port_Stream))
                        changeRoute.set()
                    if(changeRoute.isSet()):
                        predEmitter = rotaSelect[-1]
                        if(len(target)>0):
                            self.udpsocket.sendto(str('stepup').encode(),(predEmitter, Port_Stream)) 
                        changeRoute.clear()
            except:
                pass
                #print('Sem rota ainda')
    
    def AddTarget(self, addr):
        global target
        if(self.active):
            # verificar se esse enderco ja se encontra na lista de tragets
            # se nao entao adiciona
            if(not self.verifIfthisTargetExist(addr)):
                target.append(addr)
                print('adiconou target')
        else:
            target.append(addr)
            print('adiconou target')
    
    def main(self):
        global target
        threading.Thread(target=self.refresEmiiterStream).start()
        print('Encaminhamento do Stream ativado')
        while True:
            self.activeOrNo()
            packet, addr = self.udpsocket.recvfrom(BUFF_SIZE)
            if packet:
                try:
                    packet_decoded = packet.decode('utf-8')
                    #print(packet_decoded)
                    #print(f"Rota selecionada {rotaSelect}")
                    # Se receber informação em vez do packet de vídeo:
                    # as opcoes sao stepup, pause
                    if (packet_decoded[0] == 's'):
                        threading.Thread(target=self.AddTarget, args=(addr,)).start()
                        print('iniciar Enacminhamento ate o servidor')
                        #target.append(addr[0])
                        if(not self.active and (not (rotaSelect[-1] in target))):
                            #print('vai para o servidor')
                            self.sentToServer(packet)
                            #print('foi para o servidor')
                    else:
                        #depois colocar um tratamento aqui
                        target.remove(addr)
                        if(len(target) == 0):
                            self.sentToServer(packet)
                except:
                    print(f"Rota selecionada : {rotaSelect}")
                    print(' ')
                    print(f"origem : {rotaSelect[-1]}; destinos : {target}")
                    print(' ')
                    self.forwardingStream(packet)
                    #threading.Thread(target=self.forwardingStream, args=(packet)).start()
            else:
                print('Pacote Vazio')

class BuildRoute:
    def __init__(self, sk):
        self.tcpSocket = sk#socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Adiciona uma nova rota
    def AddRoute(self, routa):
        global routers
        global count
        global rotaSelect
        if(not self.thisRouteExist(routa)):
            routers[count] = routa
            count += 1
            #selecionara a melhor rota com base nos saltos
            rotaSelect = Monitor.selectBestRouteByJump(routers)
        
    # essa funcao verifica se na tabela de rotas essa rota j existe
    def thisRouteExist(self, rota):
        global routers
        verif = False
        if(count > 0):
            for i in range(count):
                if(rota == routers[i]):
                    verif = True
                    break
        return verif
    
    # Essa funcao envia a rota ate o presente no, para todos os vizinhos
    #execepto para o que enviou a mensagem
    def sendToNeighbors(self, routa):
        global neighbors
        global myIP
        routa = routa + [myIP]
        print(routa)
        sdata = pickle.dumps(routa)
        print(routers)
        print(time())
        for x in neighbors:
            if(not (x in routa)):
                print(x)
                #"""
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((x,Port_Monitor))
                #time.sleep(1)
                s.send(sdata)
                sleep(1)
                s.close()#"""
    
    # Essa funcao recebe a rota e decodifica, 
    # e chama tds as outras
    def listenNeighbors(self, conn):
        data = conn.recv(BUFF_SIZE)
        #try:
        if data:
            sdata = pickle.loads(data)
            if( type(sdata)  == type(list())):
                self.AddRoute(sdata)
                #print(type(sdata))
                #t = sdata + [myIP]
                #print(t)
                th =  threading.Thread(target=self.sendToNeighbors, args=(sdata,))
                th.start()
            elif( type(sdata) == type(str())):
                pass
            else:
                print('o tipo: '+type(sdata))
        else:
            print('Pacote Vazio')
        #except:
        #    print('erro na decodificacao')
    
    def main(self):
        # vamos colocar uma variavel booleana do while e ele vai para 
        #quando tds a rotas tiverem formadas
        while True:
            self.tcpSocket.listen(5)
            conn, addr = self.tcpSocket.accept()
            #threading.Thread(target=ServerRoute.main)
            th = threading.Thread(target=self.listenNeighbors, args=(conn,))
            th.start()
            

class Bootstrap:
    def __init__(self, sk):
        #quantidade de vizinhos
        #self.n_neighbors = 0
        self.dst = None
        #quantidade de conxoes por no
        self.__tcpsocket =  sk['tcpSocket']
        self.__neighbors_addr = []
        
    def Sendtcp(self):
        data_send = pickle.dumps(self.__neighbors_addr)
        try:
            self.__tcpsocket.sendto(data_send, self.dst)
        except:
            print('envio com os dados dos vizinhos falhou')
    
    def Getneighbors(self):
        # A variavel dst contem o par ip:porta de quem fez o pedido, o que e feito e ir a lista buscar vizinhos
        self.__neighbors_addr = nodes_neighbors[self.dst[0]]#Test[self.dst[0]]
        #self.__neighbors_addr = Test[self.dst[0]]
    
    def main(self):
        while True:
            try:
                msg, addr = self.__tcpsocket.recvfrom(1024)
                self.dst = addr
                self.Getneighbors()
                self.Sendtcp()
            except:
                print('erro ao madar vizinhos')
                break
        self.__tcpsocket.close()    
    
# A rota selecionada para enviar os pacotes
rotaSelect : list
# numero de Saltos ate o servidor
num_jumps : int
# Tabela de Rotas
routers : dict
# Todos os vizinhos do presente no, informacao vem do bootstrap
neighbors : list
# O IP do presente NO
myIP : str
# Numero de rotas, comeca em 0
count : int
# Todos os nos que vao receber encaminhamento do stream
target : list
# Tabela de Rotas com o Tempo
routesMonitor : dict
#contador para rotas com tempo
count2 : int
# Varivel que guarda o primeiro emmissor do stream para esse no
predEmitter : str
# flag que marca a mudanca de rota, quando ela e ativada e mandada para o no emmissor o pedido para parar de enviar
changeRoute : threading.Event()
# flag que diz que que marca o primeiro boot

def main():
    global changeRoute
    global predEmitter
    global neighbors
    global routers
    global myIP
    global count
    global target
    global rotaSelect
    global routesMonitor
    global count2
    predEmitter = ''
    routesMonitor = {}
    rotaSelect = []
    target = []
    count = 0
    count2 = 0
    routers = {}
    myIP = sys.argv[2]
    changeRoute = threading.Event()
    
    #Bootstrap
    #368 e 435, Teste e Final
    try:
        # argv[1] ->  ou -bt a dizer q e o bootstrap ou o ip do bootstrapper
        if(sys.argv[1] == '-bt'):
            tcpBootSocket = {}
            print('bootstrap ativado')
            #ThisNodeAddr = 
            #neighbors = Test[sys.argv[2]] #teste
            neighbors = nodes_neighbors[sys.argv[2]] #Final
            #print(f"{Port_Boot}")
            tcpBootSocket['tcpSocket'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
            tcpBootSocket['tcpSocket'].bind((sys.argv[2], Port_Boot))
            server_boot = Bootstrap(tcpBootSocket)
            tcpBootSocket['worker'] = threading.Thread(target=server_boot.main, args = ())
            tcpBootSocket['worker'].start()
            #s = int(1)/int(0) erro proposital
            #print('Fim')
            pass
        else:
            tcpBootSocket = {}
            tcpBootSocket['tcpSocket'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tcpBootSocket['tcpSocket'].bind((sys.argv[2], Port_Boot))
            tcpBootSocket['tcpSocket'].sendto((str('boot')).encode(), (sys.argv[1], Port_Boot))
            msg, addr = tcpBootSocket['tcpSocket'].recvfrom(BUFF_SIZE)
            v = pickle.loads(msg)
            neighbors = v
            #print(neighbors[0])
    except:
        print('erro no BootStrap')
    
    """
    # construindo Rotas
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((myIP, Port_Monitor))
    ServerRoute = BuildRoute(s)
    RouteThread = threading.Thread(target=ServerRoute.main)
    RouteThread.start()
    #"""
    
    #monitoramento
    tcpMonitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpMonitor.bind((myIP,Port_realMonitor))
    ServiceMonitor = Monitor(tcpMonitor)
    thMonitor = threading.Thread(target=ServiceMonitor.main)
    thMonitor.start()
    
    #Encaminhando o stream
    udpsocketStream = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsocketStream.bind((sys.argv[2], Port_Stream))
    videoStream = Stream(udpsocketStream)
    serviceForwarding = threading.Thread(target=videoStream.main) 
    serviceForwarding.start()
    
    """
    #monitoramento
    tcpMonitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpMonitor.bind((myIP,Port_realMonitor))
    ServiceMonitor = Monitor(tcpMonitor)
    thMonitor = threading.Thread(target=ServiceMonitor.main)
    thMonitor.start()
    #"""
    
if __name__ == "__main__":
	main()
    