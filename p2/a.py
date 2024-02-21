from enlace import *
import time
import numpy as np

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

        # Ativa comunicao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("Abriu a comunicação")
        
        # String a ser enviada
        string_to_send = "Hello, world!"
        print("Enviando:", string_to_send)
        
        # Convertendo a string para bytes
        txBuffer = string_to_send.encode('utf-8')
        
        print("Iniciando a transmissão...")
        com1.sendData(np.asarray(txBuffer))
        
        # Aguardando a transmissão ser concluída
        while com1.tx.threadMutex:
            time.sleep(0.05) 
        
        txSize = com1.tx.getStatus()
        print('Envio completo. Tamanho enviado:', txSize)
            
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()