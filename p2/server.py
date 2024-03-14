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

def verifica_eop(data):
    size = len(data)
    eop = data[size-4:size]

    return eop == b'\xFF\xaa\xff\xaa'

def monta_mensagem(head, payload = b'', eop = b'\xFF\xaa\xff\xaa'):
    mensagem = head + payload + eop
    return mensagem

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

        msg_t1, _ = com1.getData(14)
        time.sleep(.1)

        id = msg_t1[1]
        total_pacotes = msg_t1[2]
        nome = msg_t1[3]

        eop = b'\xFF\xaa\xff\xaa'

        msg_t2 = monta_mensagem(head=b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        com1.sendData(msg_t2)
        time.sleep(.1)

        i = 0
        while i < total_pacotes:
            mensagem_invalida = True
            while mensagem_invalida:
                start_time = time.time()
                wait = True

                while wait:
                    if time.time() - start_time > 3:
                        wait = False

                msg_t3_head = com1.getData(10)

                id = msg_t3_head[1]
                payload_size = msg_t3_head[4]

                msg_t3_payload, _ = com1.getData(payload_size)
                time.sleep(.1)

                msg_t3_eop, _ = com1.getData(4)
                time.sleep(.1)

                if msg_t3_eop == eop and id == i:
                    mensagem_invalida = False
                else:
                    msg_t6 = monta_mensagem(head=b'\x06\x00\x00\x00\x00\x00'+ i + b'\x00\x00\x00')
                    com1.sendData(msg_t6)
                    time.sleep(.1)
            msg_t4 = monta_mensagem(head=b'\x04'+ i + '\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            com1.sendData(msg_t4)
            time.sleep(.1)
            i += 1

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
