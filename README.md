# ESRTPF

  O presente trabalho foi feito no ambito da unidade curricular de engenharia e serviços em rede, tendo como objetivo implementar uma OTT para distribuição de stream em tempo real.

## Membros do Grupo:

* [Alexandre Rosa](https://github.com/Alebep/)
* [Isaías Eurico](https://github.com/isaiaseurico)
* [Marcos Mussungo](https://github.com/Firewall-Shodan)

## Objetivo

Usando primariamente o emulador CORE como bancada de teste, e uma ou mais topologias de teste, pretende-se conceber um
protótipo de entrega de vídeo com requisitos de tempo real, a partir de um servidor de conteúdos para um conjunto de
N clientes. Para tal, um conjunto de nós pode ser usado no reenvio dos dados, como intermediários, formando entre si uma rede
de overlay aplicacional, cuja criação e manutenção deve estar otimizada para a missão de entregar os conteúdos de forma mais eficiente, com o menor atraso e a largura de banda necessária. A forma como o overlay aplicacional se constitui e se organiza é determinante para a qualidade de serviço que é capaz de suportar

## COMO EXECUTAR:
  
  - `O primeiro passo é executar o ficheiro OverlayRouter nos nós intermediarios:`

      O nó bootstrapper(só podemos ter um nó bootstrap):
  
        $: python3 OverlayRouter.py -bt <ip do nó>
    Outros nós:
  
        $: python3 OverlayRouter.py <ip do bootstrapper> <ip do nó>
  - `Segundo passo rodar os codigo no(s) serviro(s):`
 
  
        $: python3 Servidor.py <ip do servidor> <ip do nó logo a frente>
  
  - `Ultimo passo, rodar nos clientes:`
  
  
        $: python3 Cliente.py <ip do nó que vai fornecer o stream>
