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

        comandos_bytearray = [ b'\x00\x00\x00\x00', b'\x00\x00\xFF\x00' ,b'\xFF\x00\x00', b'\x00\xFF\x00' , b'\x00\x00\xFF', b'\x00\xFF ', b'\xFF\x00', b'\x00',b'\xFF' ]
        mensagem = b''
        n_comandos = random.randint(10, 30)
        print("o numero de comandos sorteados foi ", n_comandos)

        for i in range(n_comandos):
            indice = random.randint(0, 8)
            mensagem = mensagem + comandos_bytearray[indice] + b'\xaa'
        
        #print(mensagem)

        caracteres = len(mensagem)
        bi = bin(caracteres)[2:]
        b = bi.zfill(8)
        inteiro = int(b, 2)
        byte_array = inteiro.to_bytes((len(b) + 7) // 8, 'big')
        mensagem = byte_array + mensagem
     
        #print("meu array de bytes tem tamanho {}" .format(len(mensagem)))       
            
        print("Iniciando a transmissão da mensagem...")
        com1.sendData(np.asarray(mensagem)) 
        
        #----------------------------------------------------
        while com1.tx.threadMutex:
            time.sleep(0.05) 
        #---------------------------------------------------- 
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
            
        print("A recepção da resposta vai começar...")
        print("esperando 1 byte de sacrifício")
        
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

                if int.from_bytes(tamanho, byteorder='big') == n_comandos:
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
