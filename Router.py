import socket, tkinter, sys, pickle, threading
import netifaces as ni
from RtpPacket import RtpPacket
from time import time, sleep
from Vars import *
""" 
Um ideia valida e termos para cada no uma lista 
serve_node-> essa lista ia guardar as rotas do servidor ate aquele no
client_node-> a rota do cliente ate aqule no.

so guarda rota completa, o no ligado a um cliente

juntar as duas para termos a rota de uma ponta a outra 

o cliente manda um pedido (ex:stepup), o node recebe e envia recursivamente,

"""
class Monitor:
    def __init__(self, sk):
       self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       #self.rotas = rotas
    
    def sendPacket(self):
         for x in rotas:     
             self.tcpSocket.sendto((str((time()))).encode(), address)
    
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
                self.udpsocket.sendto(packet, (x, Port_Stream))
    
    def sentToServer(self, packet):
        self.udpsocket.sendto(packet,(rotaSelect[-1],Port_Stream))
        
    def verifIfthisTargetExist(self):
        pass
    
    def main(self):
        global target
        while True:
            self.activeOrNo()
            packet, addr = self.udpsocket.recvfrom(BUFF_SIZE)
            if packet:
                try:
                    packet_decoded = packet.decode('utf-8')
                    # Se receber informação em vez do packet de vídeo:
                    # as opcoes sao stepup, pause
                    if packet_decoded[0]=='s':
                        target.append(addr[0])
                        if(not self.active):
                            self.sentToServer(packet)
                    else:
                        target.remove(addr[0])
                        if(len(target) == 0):
                            self.sentToServer(packet)
                except:
                    self.forwardingStream(packet)
            else:
                print('Pacote Vazio')

class BuildRoute:
    def __init__(self, sk):
        self.tcpSocket = sk#socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Adiciona uma nova rota
    def AddRoute(self, routa):
        global routers
        global count
        if(not self.thisRouteExist(routa)):
            routers[count] = routa
            count += 1
        
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
        self.__neighbors_addr = Test[self.dst[0]]
    
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
        
def mainOrigal():
    #ip da interface do proprio router definido
    router_gateway = sys.argv[1]
    num_jumps = 0
    rotas = ''
    jumps_not_received = True
    routes_not_received = True
    """Open RTP socket binded to a specified port."""
    # Create a new datagram socket to receive and send RTP packets.
    rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the timeout value of the socket to 0.5sec
    rtpSocket.settimeout(120)

    try:
        # Bind the socket to the address using the RTP port
        rtpSocket.bind((sys.argv[1], 9999))
        print('\nBind \n')
        while True:
            """Listen for RTP packets"""
            data = rtpSocket.recv(20480)
            try:
                packet_decoded = data.decode('utf-8')
                # Se receber informação em vez do packet de vídeo:
                if packet_decoded[0]=='S':
                    if routes_not_received:
                        rotas = packet_decoded + ' -> ' + router_gateway
                        routes_not_received=False
                else:
                    if jumps_not_received:
                        num_jumps = int(packet_decoded) + 1
                        jumps_not_received = False
            except:
                # Caso contrário recebe o packet com o vídeo.
                packet = data
                # Enviar para os próximos nós a stream de vídeo
                # bem como informação acerca das rotas e do nº de saltos.
                for i in range(2,len(sys.argv)):
                    rtpSocket.sendto(packet,(sys.argv[i],9999))
                    # Enviar o nº de jumps para o próximo nó do fluxo.
                    if jumps_not_received==False:
                        rtpSocket.sendto(bytes(str(num_jumps),'utf-8'),(sys.argv[i],9999))
                    # Enviar o percurso atual da rota para o próximo nó do fluxo.
                    if routes_not_received==False:
                        rtpSocket.sendto(bytes(rotas,'utf-8'),(sys.argv[i],9999))
                    print("Nº Saltos:",num_jumps)
                    print('Rotas:',rotas)
    except:
        tkinter.messageBox.showwarning('Unable to Bind', 'Unable to bind PORT=9999')
    
    # Close the RTP socket
    rtpSocket.close()

    print("All done!")

def Encaminhamento(ip_node):
    global rotaSelect
    global num_jumps
    global rotas
    rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtpSocket.settimeout(120)
    try:
        """
        Para resolver o facto de termos dois servidore
        vamos ter dois bind um para cada porta, e vamos criar uma flag
        que seleciona que seleciona qual escolher.
        """
        # Bind the socket to the address using the RTP port
        rtpSocket.bind((ip_node, Port_Stream))
        print('\nBind \n')
        while True:
            """Listen for RTP packets"""
            data = rtpSocket.recv(BUFF_SIZE)
            # packet com o vídeo.
            packet = data
            # envia para o ultimo elemento da lista com a melhor rota
            rtpSocket.sendto(packet,(rotaSelect[-1],9999))
            print("Nº Saltos:",num_jumps)
            print('Rotas:',rotas)
    except:
        tkinter.messageBox.showwarning('Unable to Bind', 'Unable to bind PORT={0}'.format(Port_Stream))
    
    # Close the RTP socket
    rtpSocket.close()

    print("All done!")
    
    
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

def main():
    global neighbors
    global routers
    global myIP
    global count
    count = 0
    routers = {}
    myIP = sys.argv[2]
    #codigo tcp
    """try:
        if sys.argv[1] == '-bt':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((sys.argv[2], 22668))
            #sock.recvfrom(1024)
            sock.listen(2)
            conn, addr = sock.accept()
            l = c.recv(1024)
    except:
        print('erro')
    """
    try:
        # argv[1] ->  ou -bt a dizer q e o bootstrap ou o ip do bootstrapper
        if(sys.argv[1] == '-bt'):
            tcpBootSocket = {}
            print('bootstrap ativado')
            #ThisNodeAddr = 
            neighbors = Test[sys.argv[2]]
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
    #"""
    # construindo Rotas
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((myIP, Port_Monitor))
    ServerRoute = BuildRoute(s)
    RouteThread = threading.Thread(target=ServerRoute.main)
    RouteThread.start()
    
    #selecionara a melhor rota com base nos saltos
    rotaSelect = Monitor.selectBestRouteByJump(routers)
    
    #Encaminhando o stream
    
    
    
if __name__ == "__main__":
	main()
    