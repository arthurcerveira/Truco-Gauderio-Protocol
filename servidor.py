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

        elif chave == "JC1":
            # Servidor começou o turno e aguarda resposta do cliente
            print(f"Cliente escolheu a carta {conteudo}")

            # Recebe carta do cliente após ter jogado carta
            carta2 = truco.cliente.cartas[int(conteudo)]

            # Remove carta do cliente da mão do cliente
            truco.cliente.cartas[int(conteudo)] = ""

            # Compara com carta na mesa
            carta1 = truco.cartas_na_mesa[truco.servidor]

            # Verifica qual carta é maior
            if carta1 > carta2:
                resposta = f"{carta1} é maior que {carta2}\n"

                # Atualiza pontuação da rodada
                truco.pontuacao_rodada[truco.servidor] += 1

                proximo_jogador = truco.servidor.nome

            elif carta2 > carta1:
                resposta = f"{carta2} é maior que {carta1}\n"

                # Atualiza pontuação da rodada
                truco.pontuacao_rodada[truco.cliente] += 1

                proximo_jogador = truco.cliente.nome

            else:
                reposta = "As duas cartas tem o mesmo valor\n"

                proximo_jogador = truco.servidor.nome

            resposta += f"Pontuação da rodada:\n" + \
                        f"Servidor = {truco.pontuacao_rodada[truco.servidor]}\n" + \
                        f"Cliente  = {truco.pontuacao_rodada[truco.cliente]}\n"

            print(resposta)

            # Verifica se rodada acabou (pontuação ou número de cartas)
            pontos = truco.pontuacao_rodada.values()
            if 2 in pontos:
                if truco.pontuacao_rodada[truco.servidor] == 2:
                    ganhador = truco.servidor.nome
                else:
                    ganhador = truco.servidor.nome

                ganhador_rodada = f"Fim da rodada. Ponto para {ganhador}"
                print(ganhador_rodada)
                resposta += ganhador_rodada

                # Se rodada acabou, verifica próximo jogador
                pass
            else:
                if proximo_jogador == truco.servidor.nome:
                    # Servido joga a próxima carta
                    # Escolhe carta
                    carta = truco.servidor.escolhe_carta()
                    truco.cartas_na_mesa[truco.servidor] = carta

                    # Resposta do cliente inicia com chave JS1
                    resposta = "JS1\n" + resposta

                    # Envia carta na mesa
                    resposta += f"Servidor jogou a carta {carta}\n"

                    # Envia para cliente suas cartas
                    resposta += mostrar_cartas(cartas_cliente)
                    resposta += "Escolha sua carta:"

                else:
                    # Cliente joga a próxima carta
                    pass
                # Senão continuar rodada
                # Jogador que ganhou o turno joga novamente

        elif chave == "JC2":
            print(conteudo)

            resposta = "Resposta JC2"

            # Cliente começou o turno e aguarda resposta do servidor
            # Escolhe carta
            # Verifica qual carta é maior
            # Atualiza pontuação da rodada
            # Verifica se rodada acabou (pontuação ou número de cartas)
            # Se rodada acabou, verifica próximo jogador
            # Senão continuar rodada
            # Jogador que ganhou o turno joga novamente
            pass

        conexao.sendall(bytes(resposta, encoding="utf-8"))

    conexao.close()

    servidor.close()
