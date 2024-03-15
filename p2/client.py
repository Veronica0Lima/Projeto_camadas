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

def verifica_eop(eop_recebido, eop = b'\xFF\xaa\xff\xaa'):
    if eop_recebido == eop:
        return True
    return False

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
        imgA = "./2.jpg"
        name_f = b'\x01'
        eop = b'\xFF\xaa\xff\xaa'
        i1 = 1
        i2 = 1
        sai = True

        
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
                print("CCCCCCCCCCCCCCCCC", i1)

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
                while sai:
                    l = com1.rx.getBufferLen()
                    if l > 0 and (time.time() - start_time) < 3 and (time.time() - tempo_inicial) < 10:                        
                        resposta_intermediaria, a = com1.getData(14)
                        print(resposta_intermediaria, a)
                        eop = verifica_eop(resposta_intermediaria[-4:])

                        # Caso o server mande que recebeu com erro - manda o mesmo pacote de novo
                        if resposta_intermediaria[0] == 6:
                            #if resposta_intermediaria[1] == i1:
                            #com1.clearBuffer()
                            if resposta_intermediaria[3] == 1:
                                mensagem = "o erro foi no tamanho do arquivo, no pacote {0}, as {1}\n".format(i1, time.time()) 
                            else:
                                mensagem = "o erro foi na ordem do pacote, no pacote {0}, as {1}\n".format(i1, time.time()) 
                            with open("log1_client.txt", "a") as arquivo:
                                arquivo.write(mensagem)
                            com1.rx.clearBuffer()
                            break

                        # Indo para o próximo arquivo caso o server diga que ta tudo ok 
                        elif resposta_intermediaria[0] == 4:
                            i1 += 1
                            sai = True
                            #com1.clearBuffer()
                            com1.rx.clearBuffer()
                            break

                        
                    elif time.time() - start_time >= 3:
                        com1.sendData(mensagem3)                   
                        start_time = time.time() 

                    elif time.time() - tempo_inicial >= 10:
                        print("-------------------------")
                        print(" Tempo excedido.")
                        print("-------------------------")
                        head5 = b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        mensagem5 = monta_mensagem(head5)
                        com1.sendData(mensagem5)
                        sai = False
                        break
                print(head3)
                if sai == False:
                    print( 'saiuuuuuuuuuuuuuuuuuuuuuuuuu')
                    break

        packages_f = divisor_bytes(imgA)
        print("tenho {} pacotes no primeiro arquivo" .format(len(packages_f)))
        tam_pl = len(packages_f)

        size_pl = tam_pl.to_bytes(1, byteorder='big')

        # Mandando mensagem avisando que vai começar
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        head1 = b'\x01\x00'+ size_pl + name_f + b'\x00\x00\x00\x00\x00\x00'
        mensagem1 = monta_mensagem(head1)
        
        com1.sendData(mensagem1)

        # Esperando mensagem falando que ta tudo ok pra receber
        resposta_inicial, _ = com1.getData(14)
        print(resposta_inicial)

        if resposta_inicial[0] == 2:

            while i2 <= tam_pl:
                print("CCCCCCCCCCCCCCCCC", i2)

                # pegando o identificador do pacote atual
                id_atual = i2.to_bytes(1, byteorder='big')

                # pegando o tamanho do pacote
                pacote_atual = packages_f[i2-1]
                tam_pac = len(pacote_atual)
                tam_pac = tam_pac.to_bytes(1, byteorder='big')

                #monstando a mensagem e enviando 
                head3 = b'\x03' + id_atual + size_pl + name_f + tam_pac + b'\x00\x00\x00\x00\x00'

                mensagem3 = monta_mensagem(head3, pacote_atual)

                com1.sendData(mensagem3)
                start_time = time.time()
                tempo_inicial = time.time()

                # Loop para aguardar a resposta com timeout de 5 segundos
                while sai:
                    l = com1.rx.getBufferLen()
                    if l > 0 and (time.time() - start_time) < 3 and (time.time() - tempo_inicial) < 10:                        
                        resposta_intermediaria, a = com1.getData(14)
                        print(resposta_intermediaria, a)
                        eop = verifica_eop(resposta_intermediaria[-4:])

                        # Caso o server mande que recebeu com erro - manda o mesmo pacote de novo
                        if resposta_intermediaria[0] == 6:
                            #if resposta_intermediaria[1] == i1:
                            #com1.clearBuffer()
                            if resposta_intermediaria[3] == 1:
                                mensagem = "o erro foi no tamanho do arquivo, no pacote {0}, as {1}\n".format(i2, time.time()) 
                            else:
                                mensagem = "o erro foi na ordem do pacote, no pacote {0}, as {1}\n".format(i2, time.time()) 
                            with open("log2_client.txt", "a") as arquivo:
                                arquivo.write(mensagem)
                            break

                        # Indo para o próximo arquivo caso o server diga que ta tudo ok 
                        elif resposta_intermediaria[0] == 4:
                            i2 += 1
                            sai = True
                            #com1.clearBuffer()
                            break

                        
                    elif time.time() - start_time >= 3:
                        com1.sendData(mensagem3)                   
                        start_time = time.time() 

                    elif time.time() - tempo_inicial >= 10:
                        print("-------------------------")
                        print(" Tempo excedido.")
                        print("-------------------------")
                        head5 = b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        mensagem5 = monta_mensagem(head5)
                        com1.sendData(mensagem5)
                        sai = False
                        break
                print(head3)
                if sai == False:
                    print( 'saiuuuuuuuuuuuuuuuuuuuuuuuuu')
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
