from socket import *

from truco.truco_gauderio import Truco
from truco.mensagens import IJ, JC1, JC2, TRUCO, RTRUCO


port = 6050

nome_host = gethostname()
host = gethostbyname(nome_host)

print(f"Host: {host}")

truco = Truco()
# Inicializa resposta como None
resposta = "None"

# Mensagens é um expedidor de mensagens pelo tipo
mensagens = {
    "IJ": IJ,
    "JC1": JC1,
    "JC2": JC2,
    "TRUCO": TRUCO,
    "RTRUCO": RTRUCO,
}

while True:
    servidor = socket(AF_INET, SOCK_STREAM)

    servidor.bind((host, port))
    servidor.listen()
    conexao, endereco = servidor.accept()

    while True:
        dados = conexao.recv(1024)

        if not dados:
            break

        mensagem = dados.decode("utf-8")

        # Primeira palavra antes do espaço representa a tipo de mensagem
        tipo_mensagem, conteudo = mensagem.split('|')

        funcao_mensagem = mensagens.get(tipo_mensagem)

        if funcao_mensagem is not None:
            resposta = funcao_mensagem(
                truco, conteudo, tipo_mensagem, resposta
            )
        # Chave não está em mensagens
        else:
            resposta = "MD|Tipo de mensagem desconhecida"
            print("Tipo de mensagem desconhecida")
            print(conteudo)

        conexao.sendall(bytes(resposta, encoding="utf-8"))

    conexao.close()

    servidor.close()
