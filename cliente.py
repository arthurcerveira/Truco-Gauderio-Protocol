from socket import *


# host = '172.17.0.3'
host = '127.0.1.1'
port = 6050

print("Digite IJ para inciar o jogo de Truco Gaudério:")
mensagem = str()

tipos_resposta = {
    "JS1": "JC1|",
    "JS2": "JC2|",
    "TRUCO": "RTRUCO|",
    "FJ": "",
    "MD": ""
}

while True:
    cliente = socket(AF_INET, SOCK_STREAM)

    entrada = input("")
    mensagem += entrada

    # Adiciona corpo para mensagem se não tiver
    if len(mensagem.split("|")) == 1:
        mensagem += "|None"

    # Entrada TRUCO sobrescreve outras informações do corpo
    if entrada == "TRUCO":
        mensagem = "TRUCO|None"

    cliente.connect((host, port))
    cliente.sendall(bytes(mensagem, encoding='utf-8'))

    dados = cliente.recv(1024)
    resposta = dados.decode('utf-8')

    # Primeira palavra antes do espaço representa a tipo de mensagem
    tipo_mensagem, conteudo = resposta.split('|')

    tipo_resposta = tipos_resposta.get(tipo_mensagem)

    if tipo_resposta is not None:
        print(conteudo)

        # Resposta do cliente inicia com tipo da mensagem
        mensagem = tipo_resposta
    else:
        # Servidor não deve ter controle sobre o tipo de resposta
        print("Houve um erro na resposta")
        print(conteudo)

    # Fim de jogo
    if tipo_mensagem == "FJ":
        # Finaliza execução
        break

    cliente.close()
