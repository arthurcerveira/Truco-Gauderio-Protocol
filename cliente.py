from socket import *


host = '172.17.0.2'
port = 6050

print("Digite IJ para inciar o jogo de Truco Gaudério:")
mensagem = str()

while True:
    cliente = socket(AF_INET, SOCK_STREAM)

    entrada = input("")
    mensagem += entrada

    cliente.connect((host, port))
    cliente.sendall(bytes(mensagem, encoding='utf-8'))

    resposta = cliente.recv(1024)
    resposta = resposta.decode('utf-8')

    # Primeira palavra antes do espaço representa a tipo de mensagem
    tipo_mensagem, *conteudo = resposta.split('\n')
    # Remonta conteúdo para imprimir na tela
    conteudo = "\n".join(conteudo)

    # Servidor jogou a primeira carta
    if tipo_mensagem == "JS1":
        print(conteudo)

        # Resposta do cliente inicia com tipo JC1
        mensagem = "JC1\n"

        # Cliente escolhe carta na próxima iteração

    # Cliente jogou a primeira carta
    elif tipo_mensagem == "JS2":
        print(conteudo)

        # Resposta do cliente inicia com tipo JC2
        mensagem = "JC2\n"

        # Cliente escolhe carta na próxima iteração

    else:
        print("Tipo de mensagem desconhecido")
        print(conteudo)

    cliente.close()
