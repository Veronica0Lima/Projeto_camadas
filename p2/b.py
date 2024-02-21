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
        
        # Inicializa a comunicação serial
        com2 = enlace(serialName)
        com2.enable()
        print("Comunicação serial aberta")
        
        # Espera receber dados
        print("Aguardando recebimento de dados...")
        rxBuffer, nRx = com2.getData(10000)  # Aqui você define o tamanho máximo esperado dos dados recebidos
        print(f"Recebidos {nRx} bytes")
        
        # Nome do arquivo de saída
        output_filename = "./dados_recebidos.txt"
        
        # Salva os dados recebidos em um arquivo
        with open(output_filename, "wb") as f:
            f.write(rxBuffer)
        
        print(f"Dados recebidos salvos em '{output_filename}'")
        
        # Encerra a comunicação serial
        com2.disable()
        print("Comunicação serial encerrada")
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()

if __name__ == "__main__":
    main()