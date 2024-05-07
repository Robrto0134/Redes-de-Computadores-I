import tkinter as tk
import socket
import struct
import random

from tkinter import messagebox

class infoCabeçalho:
    def __init__(self):
        self.ip_orig = self.get_ip_orig() 
        self.ip_dest = socket.inet_aton('15.228.191.109')
        self.ip_prot = 17
        self.comp_udp = 11
        
        self.udp_port = 50000
        self.udp_orig_port = 59155
        self.udp_checksum = 0
        
        self.__aleatorio = None
        self.__div_aleatorio = []
    
    def get_ip_orig(self):
        #cliando um socket só pra pegar o endereço IP - para não precisar alterar quando mudar de máquina
        conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conexao.connect(("8.8.8.8", 80))
        ip_orig, _ = conexao.getsockname()
        print(ip_orig)
        conexao.close()
        return socket.inet_aton(ip_orig)

    def get_ip_dest(self):
        #método que retorna IP de destinho
        return self.ip_dest

    def get_port(self):
        #método que retorna IP de destinho
        return self.udp_port

    def first_id(self): #criando o identificador aleatório e retornando o primeiro byte
        self.__aleatorio = random.randint(1, 65535)
        self.__div_aleatorio = self.__aleatorio.to_bytes(2, byteorder='big')
        return self.__div_aleatorio[0]

    def second_id(self): #segundo byte do identificador
        return self.__div_aleatorio[1]

    def montarCabeçalho(self, msg_comp):
        # Montagem do cabeçalho completo
        return struct.pack("!4s4sHHHHHBBBB", self.ip_orig, self.ip_dest, self.ip_prot, self.comp_udp,
                            self.udp_orig_port, self.udp_port, self.comp_udp, self.udp_checksum, msg_comp, self.first_id(), self.second_id())
        #estou criando uma struct com 4Bytes do IP de origem, 4Bytes do IP de destino, 5 conjuntos de 2Bytes para dados referente a protocolo e comprimento do cabeçalho,
        #4 conjuntos de 1Byte checksum, o byte do tipo da requisição e os 2 bytes do identificador

#criação dos métodos vinculados aos botões
def data_hora():    
    byte_0 = 0b0000 #byte definindo a opção de requisição para receber data e hora

    requisiçao = cabeçalho.montarCabeçalho(byte_0)
    print(requisiçao)

    comunicacao.sendto(requisiçao, (socket.inet_ntoa(cabeçalho.get_ip_dest()), cabeçalho.get_port())) #enviando solicitação

    resposta, dados_servidor = comunicacao.recvfrom(2048) #recebendo resposta do servidor
    print(resposta)
    #for i in range(0, int(resposta[3])): #filtrando a mensagem para pegar apenas a informação
        #textbox.insert(tk.END, chr(resposta[i+4]))

def msg():
    byte_0 = 0b0001 #byte definindo a opção de requisição para mensagem motivacional
    
    requisiçao = cabeçalho.montarCabeçalho(byte_0)
    print(requisiçao)

    comunicacao.sendto(requisiçao, (socket.inet_ntoa(cabeçalho.get_ip_dest()), cabeçalho.get_port())) #enviando solicitação

    resposta, dados_servidor = comunicacao.recvfrom(2048) #recebendo resposta do servidor
    print(resposta)
    #for i in range(0, int(resposta[3])): #filtrando a mensagem para pegar apenas a informação
        #textbox.insert(tk.END, chr(resposta[i+4]))

def quant():
    byte_0 = 0b0010 #byte definindo a opção de requisição para saber a quantidade de solicitações que o servidor teve
    
    requisiçao = cabeçalho.montarCabeçalho(byte_0)
    print(requisiçao)

    comunicacao.sendto(requisiçao, (socket.inet_ntoa(cabeçalho.get_ip_dest()), cabeçalho.get_port())) #enviando solicitação

    resposta, dados_servidor = comunicacao.recvfrom(2048) #recebendo resposta do servidor
    print(resposta)
    
    total = 0
    #for i in range(0, int(resposta[3])): #filtrando a mensagem para pegar apenas a quantidade de requisições
        #total = total + (int(resposta[i+4]) * (16 ** (3 - i))) #somando os valores separados por bytes
    #textbox.insert(tk.END, total)
    
def sair(): #finalização do socket e fechamento do tkinter
    confirmacao = messagebox.askquestion('Sair da Aplicação', 'Deseja encerrar o cliente?')

    if confirmacao == 'yes':
        comunicacao.close()
        root.destroy()

#criação do socket e da Janela de interação com usuário
cabeçalho = infoCabeçalho()
root = tk.Tk()
root.title("Janela do socket UDP")
try:
    comunicacao = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) #criando o socket RAW
except socket.error as e:
    tk.messagebox.showerror(title = "Erro Socket", message = "Erro na criação do socket")

#criando botões das opções disponíveis
button_dh = tk.Button(root, text = "Data e hora", command = data_hora)
button_dh.pack(pady = 5)

button_msg = tk.Button(root, text = "Uma mensagem motivacional para o fim do semestre", command = msg)
button_msg.pack(pady = 5)

button_quant = tk.Button(root, text = "A quantidade de respostas emitidas pelo servidor até o momento", command = quant)
button_quant.pack(pady = 5)

button_out = tk.Button(root, text = "Sair", command = sair)
button_out.pack(pady = 5)

#caixa de texto que contem a informação recebida do servidor
textbox = tk.Text(root, height = 5, width = 40)
textbox.pack()

root.mainloop()
