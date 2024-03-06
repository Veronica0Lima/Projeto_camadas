from enlace import *
import time
import numpy as np
import random
serialName = "COM7"  # Verifique se esta é a porta correta para o seu sistema

def main():
    try:
        print("Iniciando o main")
        com1 = enlace(serialName)
        
        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        print("Comunicação estabelecida")
        
        print("A recepção do tamanho vai começar...")
        tam, a = com1.getData(1)
        print("Dados recebidos:", tam)

        tamanho = int.from_bytes(tam, byteorder='big') 
        print(tamanho)
        # Faça algo com os dados recebidos, como decodificação, processamento, etc.
        print("A recepção da mensagem vai começar...")
        mensagem, a = com1.getData(tamanho)
        print("Recebeu {} bytes" .format(a))
        print("Dados recebidos:", mensagem)

        partes = mensagem.split(b'\xaa')
        del partes[-1]
        print("O número de comandos recebidos é: ", len(partes))
        for comando in partes:
            print(comando)

        bi = bin(len(partes))[2:]
        b = bi.zfill(8)
        inteiro = int(b, 2)
        byte_array = inteiro.to_bytes((len(b) + 7) // 8, 'big')

        bi = bin(len(partes))[2:] 
        b = bi.zfill(8)
        inteiro = int(b, 2) +1
        byte_array_errado = inteiro.to_bytes((len(b) + 7) // 8, 'big')

        print("Iniciando a transmissão da mensagem da quantidade de comandos...")
        #----------------------- timer para atrasar
        #time.sleep(8)
        #-------------------------------------------
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        # --------------------- comando para mandar certo
        #com1.sendData(np.asarray(byte_array)) 
        #--------------------- comando para mandar errado
        com1.sendData(np.asarray(byte_array_errado)) 

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("Ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()