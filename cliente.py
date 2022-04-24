from socket import *

host = '172.17.0.2'
port = 6050

while True:
    cliente = socket(AF_INET, SOCK_STREAM)

    mensagem = input("")

    cliente.connect((host, port))
    cliente.sendall(bytes(mensagem, encoding='utf-8'))

    resposta = cliente.recv(1024)

    print(resposta.decode('utf-8'))

    cliente.close()
