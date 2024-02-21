

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
        print("Abriu a comunicação")

        comandos_bytearray = [ b'\x00\x00\x00\x00', b'\x00\x00\xFF\x00' ,b'\xFF\x00\x00', b'\x00\xFF\x00' , b'\x00\x00\xFF', b'\x00\xFF ', b'\xFF\x00', b'\x00',b'\xFF' ]
        comando_bin = []
        mensagem = b''
        n_comandos = random.randint(0, 4)
        print("o numero de comandos sorteados foi ", n_comandos)

        # for comando in comandos_hexa:
        #     decimal = int(comando, 16)
        #     binario = bin(decimal)
        #     binario = binario[2:]
        #     comando_bin.append(binario)

        #print(comandos_bytearray)

        for i in range(n_comandos):
            indice = random.randint(0, 8)
            mensagem = mensagem + comandos_bytearray[indice] + b'\x10\x10\x10\x10'
        
        print(mensagem)

        caracteres = len(mensagem)
        bi = bin(caracteres)[2:]
        b = bi.zfill(8)
        byte_array = bytearray(b, 'utf-8')

        mensagem = byte_array + mensagem

        #print("AAAAAAAAA", caracteres, b)


        # imgD = "./dr.jpeg"
        # txBuffer = open(imgD, 'rb').read()       
        # print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))       
            

        # print("Iniciando a transmissão...")
        # com1.sendData(np.asarray(mensagem)) 
        
        #----------------------------------------------------
        while com1.tx.threadMutex:
            time.sleep(0.05) 
        #---------------------------------------------------- 
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
            
    
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
