from socket import *
import time


host = '172.17.0.2'
port = 6050

print("Digite IJ para inciar o jogo de Truco Gaudério:")
mensagem = str()

while True:
    # time.sleep(0.5)

    cliente = socket(AF_INET, SOCK_STREAM)

    # entrada = input("Cliente: ")
    entrada = input("")
    mensagem += entrada

    cliente.connect((host, port))
    cliente.sendall(bytes(mensagem, encoding='utf-8'))

    resposta = cliente.recv(1024)
    resposta = resposta.decode('utf-8')

    print("Servidor: ", resposta)

    # Primeira palavra antes do espaço representa a chave
    chave, *conteudo = resposta.split('\n')
    # Remonta conteúdo para imprimir na tela
    conteudo = "\n".join(conteudo)

    if chave == "JS1":
        print(conteudo)

        # Resposta do cliente inicia com chave JC1
        mensagem = "JC1\n"

        # Cliente escolhe carta na próxima iteração

    cliente.close()
