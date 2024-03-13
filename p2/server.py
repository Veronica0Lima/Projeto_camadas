from enlace import *
import time
import numpy as np
import random


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)

        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        print("Comunicação estabelecida")

        com1.sendData(b'\x02\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00')

        para_receber = True
        while para_receber:
            h, _ = com1.getData(10)
            time.sleep(.1)

            if(h[0] == b'\x01'):
                total_pacotes = int(h[2])
                nome = h[3]

                payload, size = com1.getData(total_pacotes)
                time.sleep(.1)
            elif(h[0] == b'\x02'):
                pass
            elif(h[0] == b'\x03'):
                pass
            elif(h[0] == b'\x04'):
                pass
            elif(h[0] == b'\x05'):
                pass
            elif(h[0] == b'\x06'):
                pass

        # mensagem = b'\x01'
        # time.sleep(.1)
        # com1.sendData(mensagem)
        # time.sleep(.2)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
