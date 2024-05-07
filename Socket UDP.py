import tkinter as tk
import socket
import random

from tkinter import messagebox

class infoCabeçalho:
    def __init__(self, udp_ip, udp_port, aleatorio):
        self.__udp_ip = udp_ip
        self.__udp_port = udp_port
        self.__aleatorio = aleatorio
        self.__div_aleatorio = []

    def get_ip(self):
        return self.__udp_ip

    def get_port(self):
        return self.__udp_port

    def first_id(self):
        self.__aleatorio = random.randint(1, 65535)
        self.__div_aleatorio = self.__aleatorio.to_bytes(2, byteorder='big')
        return self.__div_aleatorio[0]

    def second_id(self):
        return self.__div_aleatorio[1]

#criação dos métodos vinculados aos botões
def data_hora():    
    byte_0 = 0b0000 #byte definindo a opção de requisição
    byte_1 = cabeçalho.first_id() #primeiro byte da identificação
    byte_2 = cabeçalho.second_id() #segundo byte da identificação
    print(byte_0, " | ", byte_1, " | ", byte_2)

    msg_comp = bytes([byte_0, byte_1, byte_2]) #juntando todos os bytes antes de enviar a requisição

    comunicacao.sendto(msg_comp, (cabeçalho.get_ip(), cabeçalho.get_port())) #enviando solicitação
    print(msg_comp, "- enviada com sucesso.")

    resposta, dados_servidor = comunicacao.recvfrom(1024) #recebendo resposta do servidor
    
    for i in range(0, int(resposta[3])): #filtrando a mensagem para pegar apenas a informação
        textbox.insert(tk.END, chr(resposta[i+4]))

def msg():
    byte_0 = 0b0001 #byte definindo a opção de requisição
    byte_1 = cabeçalho.first_id() #primeiro byte da identificação
    byte_2 = cabeçalho.second_id() #segundo byte da identificação
    print(byte_0, " | ", byte_1, " | ", byte_2)

    msg_comp = bytes([byte_0, byte_1, byte_2]) #juntando todos os bytes antes de enviar a requisição

    comunicacao.sendto(msg_comp, (cabeçalho.get_ip(), cabeçalho.get_port())) #enviando solicitação
    print(msg_comp, "- enviada com sucesso.")

    resposta, dados_servidor = comunicacao.recvfrom(1024) #recebendo resposta do servidor
    
    for i in range(0, int(resposta[3])): #filtrando a mensagem para pegar apenas a mensagem
        textbox.insert(tk.END, chr(resposta[i+4]))

def quant():
    byte_0 = 0b0010 #byte definindo a opção de requisição
    byte_1 = cabeçalho.first_id() #primeiro byte da identificação
    byte_2 = cabeçalho.second_id() #segundo byte da identificação
    print(byte_0, " | ", byte_1, " | ", byte_2)

    msg_comp = bytes([byte_0, byte_1, byte_2]) #juntando todos os bytes antes de enviar a requisição

    comunicacao.sendto(msg_comp, (cabeçalho.get_ip(), cabeçalho.get_port())) #enviando solicitação
    print(msg_comp, "- enviada com sucesso.")

    resposta, dados_servidor = comunicacao.recvfrom(1024) #recebendo resposta do servidor
    print(resposta)
    print(resposta[6])
    total = 0
    for i in range(0, int(resposta[3])): #filtrando a mensagem para pegar apenas a quantidade de requisições
        total = total + (int(resposta[i+4]) * (16 ** (3 - i))) #somando os valores separados por bytes
    textbox.insert(tk.END, total)
    
def sair(): #finalização do socket e fechamento do tkinter
    confirmacao = messagebox.askquestion('Sair da Aplicação', 'Deseja encerrar o cliente?')

    if confirmacao == 'yes':
        comunicacao.close()
        root.destroy()

#criação do socket e da Janela de interação com usuário
cabeçalho = infoCabeçalho("15.228.191.109", 50000, 0)
root = tk.Tk()
root.title("Janela do socket UDP")
try:
    comunicacao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
