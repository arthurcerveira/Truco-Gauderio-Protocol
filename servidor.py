from socket import *

port = 6050

host_nome = gethostname()
host = gethostbyname(host_nome)

print(f"Host name: {host_nome}")
print(f"Host: {host}")

while True:
    servidor = socket(AF_INET, SOCK_STREAM)

    servidor.bind((host, port))
    servidor.listen()
    conexao, endereco = servidor.accept()

    while True:
        data = conexao.recv(1024)

        if not data:
            break

        message = data.decode("utf-8")

        print(message)

        resposta = input("")

        conexao.sendall(bytes(resposta, encoding="utf-8"))

    conexao.close()

    servidor.close()
