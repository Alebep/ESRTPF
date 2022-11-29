import socket, tkinter, sys, pickle, threading
import netifaces as ni
from RtpPacket import RtpPacket
from time import time
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
    def __init__(self, rotas):
       self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.rotas = rotas
    
    def sendPacket(self):
         for x in rotas:     
             self.tcpSocket.sendto((str((time()))).encode(), address)

class BuildRoute:
    def __init__(self, sk):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def AddRoute(self, routa):
        global routers
        global count
        routersp[count] = routa
        count += 1
        
    def sendToNeighbors(self, routa):
        global neighbors
        global myIP
        routa = routa + [myIP]
        print(routa)
        sdata = pickle.dumps(routa)
        for x in neighbors:
            if(not (x in routa)):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((x,Port_Monitor))
                time.sleep(0.01)
                s.send(sdata)
                time.sleep(0.02)
                s.close()
    
    def listenNeighbors(self, conn):
        data = conn.recv(BUFF_SIZE)
        try:
            if data:
                sdata = pickle.loads(data)
                if( type(sdata)  == type(list())):
                    AddRoute(sdata)
                    th = threading.Thread(target=sendToNeighbors, args=(sdata))
                    th.start()
                elif( type(sdata) == type(str())):
                    pass
                else:
                    print('o tipo: '+type(sdata))
        except:
            print('erro na decodificacao')
    
    def main(self):
        while True:
            self.listen(5)
            conn, addr = self.accept()
            

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
    
    def Askneighborsaddress(self, dst):
        pass
    
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
                data_decoded = data.decode('utf-8')
                # Se receber informação em vez do packet de vídeo:
                if data_decoded[0]=='S':
                    if routes_not_received:
                        rotas = data_decoded + ' -> ' + router_gateway
                        routes_not_received=False
                else:
                    if jumps_not_received:
                        num_jumps = int(data_decoded) + 1
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

rotaSelect : list
num_jumps : int
routers : dict
route : list
neighbors : list
myIP : str
count : int

def main():
    global neighbors
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
    except:
        print('erro')
    #"""
if __name__ == "__main__":
	main()
    