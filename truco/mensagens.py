from truco.baralho import Carta
from .truco_gauderio import mostrar_cartas


def IJ(truco, conteudo, tipo_mensagem, resposta):
    truco.etapa_atual = "IJ"

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

    if carta == "TRUCO":
        _, mensagem = resposta.split("|")
        return f"TRUCO|{mensagem}\nServidor pediu TRUCO\n1 - Aceitar\n2 - Rejeitar\n"

    truco.cartas_na_mesa[truco.servidor.nome] = carta

    # Resposta do cliente inicia com chave JS1
    resposta = "JS1|"

    # Envia carta na mesa
    resposta += f"Servidor jogou a carta {carta}\n"

    # Envia para cliente suas cartas
    resposta += mostrar_cartas(truco.cliente.cartas)
    resposta += "Escolha sua carta:"

    return resposta


def JC1(truco, conteudo, tipo_mensagem, resposta):
    truco.etapa_atual = "JC1"

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
            "--------------------------------------\n" + \
            f"Servidor {truco.placar[truco.servidor.nome]} x " + \
            f"{truco.placar[truco.cliente.nome]} Cliente\n" + \
            "--------------------------------------\n"

        resposta += placar
        print(placar)

        resposta = truco.proxima_rodada(resposta)

    # Senão continuar rodada
    else:
        # Jogador que ganhou o turno joga novamente
        # Servido joga a próxima carta
        if proximo_jogador == truco.servidor.nome:
            truco.etapa_atual = "JC1"

            # Escolhe carta
            carta = truco.servidor.escolhe_carta()

            if carta == "TRUCO":
                try:
                    _, mensagem = resposta.split("|")
                except ValueError:
                    mensagem = ""
                return f"TRUCO|{mensagem}\nServidor pediu TRUCO\n1 - Aceitar\n2 - Rejeitar\n"

            truco.cartas_na_mesa[truco.servidor.nome] = carta

            # Resposta do cliente inicia com chave JS1
            resposta = "JS1|" + resposta

            # Envia carta na mesa
            resposta += f"Servidor jogou a carta {carta}\n"

        # Cliente joga a próxima carta
        else:
            truco.etapa_atual = "JC2"

            resposta = "JS2|" + resposta

        # Envia para cliente suas cartas
        resposta += mostrar_cartas(truco.cliente.cartas)
        resposta += "Escolha sua carta:"

    return resposta


def JC2(truco, conteudo, tipo_mensagem, resposta):
    truco.etapa_atual = "JC2"

    if conteudo == "C2RTRUCO":
        # Caso de borda para sistema de TRUCO do servidor
        carta2 = truco.cartas_na_mesa[truco.cliente.nome]
    else:
        # Recebe carta do cliente após ter jogado carta
        carta2 = truco.cliente.cartas[int(conteudo)]

        truco.cartas_na_mesa[truco.cliente.nome] = carta2

        # Remove carta do cliente da mão do cliente
        truco.cliente.cartas[int(conteudo)] = ""

    print(f"Cliente jogou a carta {carta2}")

    # Escolhe carta
    carta1 = truco.servidor.escolhe_carta()

    if carta1 == "TRUCO":
        try:
            _, mensagem = resposta.split("|")
        except ValueError:
            mensagem = ""
        return f"TRUCO|{mensagem}\nServidor pediu TRUCO\n1 - Aceitar\n2 - Rejeitar\n"

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
            "--------------------------------------\n" + \
            f"Servidor {truco.placar[truco.servidor.nome]} x " + \
            f"{truco.placar[truco.cliente.nome]} Cliente\n" + \
            "--------------------------------------\n"

        resposta += placar
        print(placar)

        resposta = truco.proxima_rodada(resposta)

    # Senão continuar rodada
    else:
        # Jogador que ganhou o turno joga novamente
        # Servido joga a próxima carta
        if proximo_jogador == truco.servidor.nome:
            truco.etapa_atual = "JC1"

            # Escolhe carta
            carta = truco.servidor.escolhe_carta()

            if carta == "TRUCO":
                try:
                    _, mensagem = resposta.split("|")
                except ValueError:
                    mensagem = ""
                return f"TRUCO|{mensagem}\nServidor pediu TRUCO\n1 - Aceitar\n2 - Rejeitar\n"

            truco.cartas_na_mesa[truco.servidor.nome] = carta

            # Resposta do cliente inicia com chave JS1
            resposta = "JS1|" + resposta

            # Envia carta na mesa
            resposta += f"Servidor jogou a carta {carta}\n"

        # Cliente joga a próxima carta
        else:
            truco.etapa_atual = "JC2"

            resposta = "JS2|" + resposta

        # Envia para cliente suas cartas
        resposta += mostrar_cartas(truco.cliente.cartas)
        resposta += "Escolha sua carta:"

    return resposta


def TRUCO(truco, conteudo, tipo_mensagem, resposta):
    aceitar_truco = input(
        "Cliente pediu TRUCO\n1 - Aceitar\n2 - Rejeitar\n"
    )

    tipo, mensagem = resposta.split("|")

    if aceitar_truco == "1":
        truco.pontos_rodada = 2

        # Reenvia mesma mensagem após confirmação
        truco_mensagem = "TRUCO aceito\nA rodada agora vale 2 pontos\n"

        resposta = f"{tipo}|{truco_mensagem}{mensagem}"
    else:
        resposta = f"TRUCO rejeitado\nPonto para cliente\n"
        print(resposta)

        # Atualiza placar
        truco.placar[truco.cliente.nome] += 1

        # Vai para próxima rodada
        placar = "Placar do jogo:\n" + \
            "--------------------------------------\n" + \
            f"Servidor {truco.placar[truco.servidor.nome]} x " + \
            f"{truco.placar[truco.cliente.nome]} Cliente\n" + \
            "--------------------------------------\n"

        resposta += placar
        print(placar)

        resposta = truco.proxima_rodada(resposta)

    return resposta


def RTRUCO(truco, conteudo, tipo_mensagem, resposta):
    aceitar_truco = conteudo

    # TRUCO aceito, joga carta
    if aceitar_truco == "1":
        truco.pontos_rodada = 2

        truco_mensagem = "TRUCO aceito\nA rodada agora vale 2 pontos\n"
        print(truco_mensagem)

        if truco.etapa_atual == "JC1":
            # Servidor escolhe carta
            carta = truco.servidor.escolhe_carta()

            truco.cartas_na_mesa[truco.servidor.nome] = carta

            # Resposta do cliente inicia com chave JS1
            resposta = "JS1|"

            # Envia carta na mesa
            resposta += f"Servidor jogou a carta {carta}\n"

            # Envia para cliente suas cartas
            resposta += mostrar_cartas(truco.cliente.cartas)
            resposta += "Escolha sua carta:"
        elif truco.etapa_atual == "JC2":
            # C2RTRUCO é um código para servidor pegar a carta que está na mesa
            resposta = JC2(truco, "C2RTRUCO", tipo_mensagem, resposta)

        tipo, mensagem = resposta.split("|")
        resposta = f"{tipo}|{truco_mensagem}{mensagem}"
    # TRUCO rejeitado, vai para próxima rodada
    else:
        resposta = f"TRUCO rejeitado\nPonto para servidor\n"
        print(resposta)

        # Atualiza placar
        truco.pontuacao_rodada[truco.servidor.nome] += 1

        # Vai para próxima rodada
        resposta = truco.proxima_rodada(resposta)

    return resposta
