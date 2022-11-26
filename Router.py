import socket, tkinter, sys
import netifaces as ni
from RtpPacket import RtpPacket

def main():
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

if __name__ == "__main__":
	main()