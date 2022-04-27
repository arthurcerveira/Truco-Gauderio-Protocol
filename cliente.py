from socket import *


host = '172.17.0.2'
# host = '127.0.1.1'
port = 6050

print("Digite IJ para inciar o jogo de Truco Gaudério:")
mensagem = str()

while True:
    cliente = socket(AF_INET, SOCK_STREAM)

    entrada = input("")
    mensagem += entrada

    if mensagem == "IJ":
        mensagem += "|None"

    if entrada == "TRUCO":
        mensagem = "TRUCO|None"

    cliente.connect((host, port))
    cliente.sendall(bytes(mensagem, encoding='utf-8'))

    dados = cliente.recv(1024)
    resposta = dados.decode('utf-8')

    # print("Servidor: " + resposta)

    # Primeira palavra antes do espaço representa a tipo de mensagem
    tipo_mensagem, conteudo = resposta.split('|')

    # Servidor jogou a primeira carta
    if tipo_mensagem == "JS1":
        print(conteudo)

        # Resposta do cliente inicia com tipo JC1
        mensagem = "JC1|"

        # Cliente escolhe carta na próxima iteração

    # Cliente jogou a primeira carta
    elif tipo_mensagem == "JS2":
        print(conteudo)

        # Resposta do cliente inicia com tipo JC2
        mensagem = "JC2|"

        # Cliente escolhe carta na próxima iteração

    # Cliente jogou a primeira carta
    elif tipo_mensagem == "TRUCO":
        # print(conteudo)

        print("Servidor pediu TRUCO\n1 - Aceitar\n2 - Rejeitar\n")

        # Resposta do cliente inicia com tipo RTRUCO
        mensagem = "RTRUCO|"

        # Cliente decide se quer TRUCO na próxima iteração

    # Fim de jogo
    elif tipo_mensagem == "FJ":
        print(conteudo)

        # Finaliza execução
        break

    else:
        print("Tipo de mensagem desconhecido")
        print(conteudo)

    cliente.close()
