from enlace import *
import time
import numpy as np
import random
import traceback



# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def monta_mensagem(head, payload = b'', eop = b'\xFF\xaa\xff\xaa'):
    mensagem = head + payload + eop
    return mensagem

# def get_data(com1, msg_t1):
#     id = msg_t1[0] 
#     total_pacotes = msg_t1[2]
#     nome = str(msg_t1[3])
#     nome_copia = nome + '_copia.jpeg'

#     eop = b'\xFF\xaa\xff\xaa'

#     msg_t2 = monta_mensagem(head=b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
#     com1.sendData(msg_t2)
#     time.sleep(.1)

#     i = 0
#     sai = True
#     print(total_pacotes)

#     data_img = bytearray([])
    
#     while i < total_pacotes and sai:
#         mensagem_invalida = True
#         while mensagem_invalida:
#             #if(time.time() - start_time < 10):
#             l = com1.rx.getBufferLen()
#             start_time = time.time()
#             while (time.time() - start_time < 10):

#                 msg_t3_head, _ = com1.getData(10) 
#                 print(msg_t3_head)

#                 id = msg_t3_head[1]
#                 payload_size = msg_t3_head[4]

#                 msg_t3_payload, _ = com1.getData(payload_size)
#                 msg_t3_eop, _ = com1.getData(4)
#                 print(msg_t3_eop)
#                 print(i)

#                 if msg_t3_eop == eop and (id == i+1):
#                     mensagem_invalida = False
#                 else:
#                     if msg_t3_eop != eop:
#                         type_error = b'\x01'
#                         mensagem = "o erro foi no tamanho do arquivo, no pacote {0}, as {1}".format(i, time.time())

#                     else:
#                         type_error = b'\x02'
#                         mensagem = "o erro foi na ordem do pacote, no pacote {0}, as {1}".format(i, time.time()) 
                        
#                     print(mensagem)
#                     with open("log1_server.txt", "w") as arquivo:
#                         arquivo.write(mensagem)
#                     msg_t6 = monta_mensagem(head=b'\x06\x00\x00' + type_error + b'\x00\x00'+ bytes([i]) + b'\x00\x00\x00')
#                     com1.sendData(msg_t6)
#                     start_time = time.time()
#                 break
#             else:
#                 msg_t5 = monta_mensagem(head=b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00')
#                 com1.sendData(msg_t5)

#                 print("-------------------------------------")
#                 print("Tempo excedido! Comunicação encerrada")
#                 print("-------------------------------------")
#                 com1.disable()
#                 sai = False
#                 break
        
#         msg_t4 = monta_mensagem(head=b'\x04'+ bytes([i]) + b'\x00\x00\x00\x00\x00\x00\x00\x00')
#         com1.sendData(msg_t4)
        
#         data_img += msg_t3_payload
#         i += 1

    with open(nome_copia, 'wb') as file:
        file.write(data_img)
    pass

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

        # begin = time.time()
        # time_control = time.time()

        # while (time.time() - time_control) < 10:
        msg_t1, _ = com1.getData(14)
        #     time.sleep(.1)

        #     if(msg_t1[0] == 1):
        #         get_data(com1, msg_t1)
        #         time_control = time.time()



        id = msg_t1[0] 
        total_pacotes = msg_t1[2]
        nome = str(msg_t1[3])
        nome_copia = nome + '_copia.jpeg'

        eop = b'\xFF\xaa\xff\xaa'

        msg_t2 = monta_mensagem(head=b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        com1.sendData(msg_t2)
        time.sleep(.1)

        i = 0
        sai = True
        print(total_pacotes)
        begin = time.time()

        data_img = bytearray([])
        
        while i < total_pacotes and sai:
            mensagem_invalida = True
            while mensagem_invalida:
                #if(time.time() - start_time < 10):
                l = com1.rx.getBufferLen()
                start_time = time.time()
                while (time.time() - start_time < 10):
                    msg_t3_head, _ = com1.getData(10) 
                    print(msg_t3_head)

                    id = msg_t3_head[1]

                    payload_size = msg_t3_head[4]

                    msg_t3_payload, _ = com1.getData(payload_size)
                    msg_t3_eop, _ = com1.getData(4)
                    print(id)
                    print(i)

                    if msg_t3_eop == eop and (id == i+1):
                        mensagem_invalida = False
                    else:
                        if msg_t3_eop != eop:
                            type_error = b'\x01'
                            mensagem = "o erro foi no tamanho do arquivo, no pacote {0}, as {1}\n".format(i, time.time())

                        else:
                            type_error = b'\x02'
                            mensagem = "o erro foi na ordem do pacote, no pacote {0}, as {1}\n".format(i, time.time()) 
                            
                        print(mensagem)
                        with open("log1_server.txt", "a") as arquivo:
                            arquivo.write(mensagem)
                        msg_t6 = monta_mensagem(head=b'\x06\x00\x00' + type_error + b'\x00\x00'+ bytes([i]) + b'\x00\x00\x00')
                        com1.sendData(msg_t6)
                        start_time = time.time()
                    break
                else:
                    msg_t5 = monta_mensagem(head=b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00')
                    com1.sendData(msg_t5)

                    print("-------------------------------------")
                    print("Tempo excedido! Comunicação encerrada")
                    print("-------------------------------------")
                    com1.disable()
                    sai = False
                    break
            
            msg_t4 = monta_mensagem(head=b'\x04'+ bytes([i]) + b'\x00\x00\x00\x00\x00\x00\x00\x00')
            com1.sendData(msg_t4)            
            data_img += msg_t3_payload
            i += 1

        with open(nome_copia, 'wb') as file:
            file.write(data_img)
        mensagem = b'\x01'
        time.sleep(.1)
        com1.sendData(mensagem)
        time.sleep(.2)

        msg_t1, _ = com1.getData(14)

        id = msg_t1[0] 
        total_pacotes = msg_t1[2]
        nome = str(msg_t1[3])
        nome_copia = nome + '_copia.jpg'

        msg_t2 = monta_mensagem(head=b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        com1.sendData(msg_t2)
        time.sleep(.1)

        i = 0
        sai = True
        print(total_pacotes)
        begin = time.time()

        data_img = bytearray([])
        
        while i < total_pacotes and sai:
            mensagem_invalida = True
            while mensagem_invalida:
                #if(time.time() - start_time < 10):
                l = com1.rx.getBufferLen()
                start_time = time.time()
                while (time.time() - start_time < 10):
                    msg_t3_head, _ = com1.getData(10) 
                    print(msg_t3_head)

                    id = msg_t3_head[1]

                    payload_size = msg_t3_head[4]

                    msg_t3_payload, _ = com1.getData(payload_size)
                    msg_t3_eop, _ = com1.getData(4)
                    print(id)
                    print(i)

                    if msg_t3_eop == eop and (id == i+1):
                        mensagem_invalida = False
                    else:
                        if msg_t3_eop != eop:
                            type_error = b'\x01'
                            mensagem = "o erro foi no tamanho do arquivo, no pacote {0}, as {1}\n".format(i, time.time())

                        else:
                            type_error = b'\x02'
                            mensagem = "o erro foi na ordem do pacote, no pacote {0}, as {1}\n".format(i, time.time()) 
                            
                        print(mensagem)
                        with open("log2_server.txt", "a") as arquivo:
                            arquivo.write(mensagem)
                        msg_t6 = monta_mensagem(head=b'\x06\x00\x00' + type_error + b'\x00\x00'+ bytes([i]) + b'\x00\x00\x00')
                        com1.sendData(msg_t6)
                        start_time = time.time()
                    break
                else:
                    msg_t5 = monta_mensagem(head=b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00')
                    com1.sendData(msg_t5)

                    print("-------------------------------------")
                    print("Tempo excedido! Comunicação encerrada")
                    print("-------------------------------------")
                    com1.disable()
                    sai = False
                    break
            
            msg_t4 = monta_mensagem(head=b'\x04'+ bytes([i]) + b'\x00\x00\x00\x00\x00\x00\x00\x00')
            com1.sendData(msg_t4)            
            data_img += msg_t3_payload
            i += 1

        with open(nome_copia, 'wb') as file:
            file.write(data_img)
        # mensagem = b'\x01'
        # time.sleep(.1)
        # com1.sendData(mensagem)
        # time.sleep(.2)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print(f"A transmissão durou {(time.time() - begin):.2f} segundos")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print(f"ops! :-{traceback.format_exc()}")
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
