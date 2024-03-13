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

def divisor_bytes(nome_arquivo, tamanho_pacote=140):
    with open(nome_arquivo, 'rb') as arquivo_origem:
        pacotes = []
        while True:
            dados = arquivo_origem.read(tamanho_pacote)
            if not dados:
                break
            pacotes.append(dados)
    return pacotes

def monta_mensagem(head, payload = b'', eop = b'\xFF\xaa\xff\xaa'):
    mensagem = head + payload + eop
    return mensagem

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        #byte de sacrifício
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        # Variáveis globais 
        imgD = "./1.jpeg"
        name_f = b'\x01'
        eop = b'\xFF\xaa\xff\xaa'
        i1 = 1
        i2 = 1
        
        # arquivo1 = open(imgD, 'rb').read()
        # print("meu array de bytes tem tamanho {}" .format(len(arquivo1)))

        
        packages_f = divisor_bytes(imgD)
        print("tenho {} pacotes no primeiro arquivo" .format(len(packages_f)))
        tam_pl = len(packages_f)

        size_pl = tam_pl.to_bytes(1, byteorder='big')

        # Mandando mensagem avisando que vai começar
        head1 = b'\x01\x00'+ size_pl + name_f + b'\x00\x00\x00\x00\x00\x00'
        mensagem1 = monta_mensagem(head1)
        com1.sendData(mensagem1)

        # Esperando mensagem falando que ta tudo ok pra receber
        resposta_inicial, _ = com1.getData(14)

        if resposta_inicial[0] == 2:

            while i1 <= tam_pl:

                # pegando o identificador do pacote atual
                id_atual = i1.to_bytes(1, byteorder='big')

                # pegando o tamanho do pacote
                pacote_atual = packages_f[i1-1]
                tam_pac = len(pacote_atual)
                tam_pac = tam_pac.to_bytes(1, byteorder='big')

                #monstando a mensagem e enviando 
                head3 = b'\x03' + id_atual + size_pl + name_f + tam_pac + b'\x00\x00\x00\x00\x00'

                mensagem3 = monta_mensagem(head3, pacote_atual)

                com1.sendData(mensagem3)
                start_time = time.time()
                tempo_inicial = time.time()

                # Loop para aguardar a resposta com timeout de 5 segundos
                while True:
                    l = com1.rx.getBufferLen()
                    if l > 0 and (time.time() - start_time) < 3 and (time.time() - tempo_inicial) < 10:
                        
                        resposta_intermediaria, _ = com1.getData(10)

                        if resposta_intermediaria[0] == 6:
                            break

                    elif time.time() - start_time >= 3:
                        com1.sendData(mensagem3)
                        start_time = time.time()
                


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
