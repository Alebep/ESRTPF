# Porta de onde passa o video
Port_Stream = 11998
BUFF_SIZE = 65536
Port_Stream2 = 11999
#Porta Construcao de Rotas
Port_Monitor = 12000
#porta BootStarp
Port_Boot = 15159


# teste
Test = {
    '10.0.0.1':['10.0.0.10','10.0.3.2','10.0.4.2'],
    '10.0.3.2':['10.0.0.1','10.0.4.2'],#'10.0.6.20'],
    '10.0.4.2':['10.0.0.1','10.0.3.2']#,'10.0.5.20']   
}

o2 = '10.0.4.1'
o3 = '10.0.5.1'
o7 = '10.0.2.1'
o5 = '10.0.11.2'
o6 = '10.0.1.1'

nodes_neighbors = {
    '10.0.4.1':['10.0.2.1','10.0.5.1'],#O2
    '10.0.5.1':['10.0.11.2','10.0.4.1'],#O3
    '10.0.2.1':['10.0.11.2','10.0.1.1','10.0.4.1'],#O7
    '10.0.11.2':['10.0.1.1','10.0.2.1','10.0.5.1'],#O5
    '10.0.1.1':['10.0.11.2','10.0.2.1']#O6
}