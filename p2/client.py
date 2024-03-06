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
serialName = "COM6"                  # Windows(variacao de)

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)

        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        print("Abriu a comunicação")

        start_time = time.time()

        # Loop para aguardar a resposta com timeout de 5 segundos
        while True:
            l = com1.rx.getBufferLen()
            if l > 0 and (time.time() - start_time) < 5:
                print("Resposta recebida com sucesso.")
                rxBuffer, nRx = com1.getData(1)
                com1.rx.clearBuffer()
                time.sleep(.1)
                tamanho, a = com1.getData(1)  
                print(int.from_bytes(tamanho, byteorder='big'))

                if int.from_bytes(tamanho, byteorder='big') == 2:
                    print('Número de comandos certo')
                else:
                    print("Número de comandos errado")
                break
            elif time.time() - start_time >= 5:
                print("Timeout excedido. Nenhuma resposta recebida.")
                break


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
