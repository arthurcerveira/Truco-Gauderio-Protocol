from uuid import RESERVED_FUTURE
from estado import Truco, Jogador, mostrar_cartas
from socket import *
from truco_gauderio import *


port = 6050

nome_host = gethostname()
host = gethostbyname(nome_host)

print(f"Host: {host}")

truco = Truco()


while True:
    # time.sleep(0.5)

    servidor = socket(AF_INET, SOCK_STREAM)

    servidor.bind((host, port))
    servidor.listen()
    conexao, endereco = servidor.accept()

    while True:
        data = conexao.recv(1024)

        if not data:
            # print("Not data")
            break

        mensagem = data.decode("utf-8")

        # print("Cliente: ", mensagem)

        # Primeira palavra antes do espaço representa a chave
        chave, *conteudo = mensagem.split('\n')
        # Remonta conteúdo para imprimir na tela
        conteudo = "\n".join(conteudo)

        if chave == "IJ":
            # Inicializa jogo
            print(f"Jogo inicializado por cliente\n")

            # Incializa placar

            # Cria baralho
            baralho = Baralho()
            baralho.embaralhar()

            # Dá as cartas
            cartas_servidor, cartas_cliente = dar_as_cartas(baralho)

            # Cria jogadores
            truco.servidor = Jogador(cartas_servidor, "Servidor")
            truco.cliente = Jogador(cartas_cliente, "Cliente")

            # Inicializa pontuação da rodada
            truco.pontuacao_rodada = {
                truco.servidor: 0,
                truco.cliente: 0
            }

            # Escolhe carta
            carta = truco.servidor.escolhe_carta()
            truco.cartas_na_mesa[truco.servidor] = carta

            # Resposta do cliente inicia com chave JS1
            resposta = "JS1\n"

            # Envia carta na mesa
            resposta += f"Servidor jogou a carta {carta}\n"

            # Envia para cliente suas cartas
            resposta += mostrar_cartas(cartas_cliente)
            resposta += "Escolha sua carta:"

            # Estado (carta na mesa, pontuacao da rodada, aguardando jogada)

        # Servidor começou o turno e aguarda resposta do cliente
        elif chave == "JC1":
            # Recebe carta do cliente após ter jogado carta
            carta2 = truco.cliente.cartas[int(conteudo)]

            print(f"Cliente jogou a carta {carta2}")

            # Remove carta do cliente da mão do cliente
            truco.cliente.cartas[int(conteudo)] = ""

            # Compara com carta na mesa
            carta1 = truco.cartas_na_mesa[truco.servidor]

            # Define maior carta e atualiza pontuação da rodada
            resposta, proximo_jogador = truco.maior_carta(carta1, carta2)

            resposta += f"Pontuação da rodada:\n" + \
                        f"Servidor = {truco.pontuacao_rodada[truco.servidor]}\n" + \
                        f"Cliente  = {truco.pontuacao_rodada[truco.cliente]}\n"

            print(resposta)

            # Verifica se rodada acabou
            fim_rodada = truco.fim_rodada(resposta)

            if fim_rodada:
                resposta += fim_rodada

            # Senão continuar rodada
            else:
                # Jogador que ganhou o turno joga novamente
                resposta += truco.proxima_jogada(resposta, proximo_jogador)

        # Cliente começou o turno e aguarda resposta do servidor
        elif chave == "JC2":
            # Recebe carta do cliente após ter jogado carta
            carta2 = truco.cliente.cartas[int(conteudo)]
            print(f"Cliente jogou a carta {carta2}")

            # Remove carta do cliente da mão do cliente
            truco.cliente.cartas[int(conteudo)] = ""

            # Escolhe carta
            carta1 = truco.servidor.escolhe_carta()

            # Verifica qual carta é maior
            carta1 = truco.cartas_na_mesa[truco.servidor]

            resposta, proximo_jogador = truco.maior_carta(carta1, carta2)

            resposta += f"Pontuação da rodada:\n" + \
                        f"Servidor = {truco.pontuacao_rodada[truco.servidor]}\n" + \
                        f"Cliente  = {truco.pontuacao_rodada[truco.cliente]}\n"

            # Verifica se rodada acabou
            fim_rodada = truco.fim_rodada(resposta)

            if fim_rodada is not None:
                resposta += fim_rodada

            # Senão continuar rodada
            else:
                # Jogador que ganhou o turno joga novamente
                resposta += truco.proxima_jogada(resposta, proximo_jogador)
        else:
            print("Chave desconhecida")
            print(conteudo)
        conexao.sendall(bytes(resposta, encoding="utf-8"))

    conexao.close()

    servidor.close()
