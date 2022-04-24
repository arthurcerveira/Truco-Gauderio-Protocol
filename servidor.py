from socket import *

from truco.truco_gauderio import Truco, Jogador, mostrar_cartas
from truco.baralho import Baralho, dar_as_cartas


port = 6050

nome_host = gethostname()
host = gethostbyname(nome_host)

print(f"Host: {host}")

truco = Truco()


while True:
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

        print("Cliente: ", mensagem)

        # Primeira palavra antes do espaço representa a tipo de mensagem
        tipo_mensagem, *conteudo = mensagem.split('\n')
        # Remonta conteúdo para imprimir na tela
        conteudo = "\n".join(conteudo)

        if tipo_mensagem == "IJ":
            # Inicializa jogo
            print(f"Jogo inicializado por cliente\n")

            # Incializa placar
            truco.placar = {
                "Servidor": 0,
                "Cliente": 0,
            }

            # Inicializa baralho, e dá cartas aos jogadores
            truco.inicializa_rodada("Servidor")

            # Escolhe carta
            carta = truco.servidor.escolhe_carta()
            truco.cartas_na_mesa[truco.servidor.nome] = carta

            # Resposta do cliente inicia com chave JS1
            resposta = "JS1\n"

            # Envia carta na mesa
            resposta += f"Servidor jogou a carta {carta}\n"

            # Envia para cliente suas cartas
            resposta += mostrar_cartas(truco.cliente.cartas)
            resposta += "Escolha sua carta:"

            # Estado (carta na mesa, pontuacao da rodada, aguardando jogada)

        # Servidor começou o turno e aguarda resposta do cliente
        elif tipo_mensagem == "JC1":
            # Recebe carta do cliente após ter jogado carta
            carta2 = truco.cliente.cartas[int(conteudo)]

            print(f"Cliente jogou a carta {carta2}")

            # Remove carta do cliente da mão do cliente
            truco.cliente.cartas[int(conteudo)] = ""

            # Compara com carta na mesa
            carta1 = truco.cartas_na_mesa[truco.servidor.nome]

            # Define maior carta e atualiza pontuação da rodada
            resposta, proximo_jogador = truco.maior_carta(carta1,
                                                          carta2,
                                                          truco.servidor.nome)

            resposta += f"Pontuação da rodada:\n" + \
                        f"Servidor = {truco.pontuacao_rodada[truco.servidor.nome]}\n" + \
                        f"Cliente  = {truco.pontuacao_rodada[truco.cliente.nome]}\n"

            print(resposta)

            # Verifica se rodada acabou
            fim_rodada = truco.fim_rodada(resposta)

            if fim_rodada:
                resposta = fim_rodada

                placar = "Placar do jogo:\n" + \
                    f"Servidor = {truco.placar[truco.servidor.nome]}\n" + \
                    f"Cliente  = {truco.placar[truco.cliente.nome]}\n" + \
                    "Começando nova rodada\n"

                resposta += placar
                print(placar)

                resposta = truco.proxima_rodada(resposta)

            # Senão continuar rodada
            else:
                # Jogador que ganhou o turno joga novamente
                resposta = truco.proxima_jogada(resposta, proximo_jogador)

        # Cliente começou o turno e aguarda resposta do servidor
        elif tipo_mensagem == "JC2":
            # Recebe carta do cliente após ter jogado carta
            carta2 = truco.cliente.cartas[int(conteudo)]
            print(f"Cliente jogou a carta {carta2}")

            # Remove carta do cliente da mão do cliente
            truco.cliente.cartas[int(conteudo)] = ""

            # Escolhe carta
            carta1 = truco.servidor.escolhe_carta()

            # Verifica qual carta é maior
            resposta, proximo_jogador = truco.maior_carta(carta1,
                                                          carta2,
                                                          truco.cliente.nome)

            resposta += f"Pontuação da rodada:\n" + \
                        f"Servidor = {truco.pontuacao_rodada[truco.servidor.nome]}\n" + \
                        f"Cliente  = {truco.pontuacao_rodada[truco.cliente.nome]}\n"

            print(resposta)

            # Verifica se rodada acabou
            fim_rodada = truco.fim_rodada(resposta)

            if fim_rodada:
                resposta = fim_rodada

                placar = "Placar do jogo:\n" + \
                    f"Servidor = {truco.placar[truco.servidor.nome]}\n" + \
                    f"Cliente  = {truco.placar[truco.cliente.nome]}\n" + \
                    "Começando nova rodada\n"

                resposta += placar
                print(placar)

                resposta = truco.proxima_rodada(resposta)

            # Senão continuar rodada
            else:
                # Jogador que ganhou o turno joga novamente
                resposta = truco.proxima_jogada(resposta, proximo_jogador)
        else:
            print("Tipo de mensagem desconhecida")
            print(conteudo)

        conexao.sendall(bytes(resposta, encoding="utf-8"))

    conexao.close()

    servidor.close()
