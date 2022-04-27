from socket import *

from truco.truco_gauderio import Truco
from truco.mensagens import IJ, JC1, JC2, TRUCO, RTRUCO


port = 6050

nome_host = gethostname()
host = gethostbyname(nome_host)

print(f"Host: {host}")

truco = Truco()
resposta = str()

while True:
    servidor = socket(AF_INET, SOCK_STREAM)

    servidor.bind((host, port))
    servidor.listen()
    conexao, endereco = servidor.accept()

    while True:
        dados = conexao.recv(1024)

        if not dados:
            # print("Not data")
            break

        mensagem = dados.decode("utf-8")

        # Primeira palavra antes do espaço representa a tipo de mensagem
        tipo_mensagem, conteudo = mensagem.split('|')

        if tipo_mensagem == "IJ":
            resposta = IJ(truco, conteudo, tipo_mensagem, resposta)

        # Servidor começou o turno e aguarda resposta do cliente
        elif tipo_mensagem == "JC1":
            resposta = JC1(truco, conteudo, tipo_mensagem, resposta)

        # Cliente começou o turno e aguarda resposta do servidor
        elif tipo_mensagem == "JC2":
            resposta = JC2(truco, conteudo, tipo_mensagem, resposta)

        # Cliente pede TRUCO
        elif tipo_mensagem == "TRUCO":
            resposta = TRUCO(truco, conteudo, tipo_mensagem, resposta)

        # Resposta do Cliente quando servidor pede TRUCO
        elif tipo_mensagem == "RTRUCO":
            resposta = RTRUCO(truco, conteudo, tipo_mensagem, resposta)

        else:
            print("Tipo de mensagem desconhecida")
            print(conteudo)

        conexao.sendall(bytes(resposta, encoding="utf-8"))

    conexao.close()

    servidor.close()
