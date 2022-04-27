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
            f"Servidor = {truco.placar[truco.servidor.nome]}\n" + \
            f"Cliente  = {truco.placar[truco.cliente.nome]}\n"

        resposta += placar
        print(placar)

        resposta = truco.proxima_rodada(resposta)

    # Senão continuar rodada
    else:
        # Jogador que ganhou o turno joga novamente
        resposta = truco.proxima_jogada(resposta, proximo_jogador)

    return resposta


def JC2(truco, conteudo, tipo_mensagem, resposta):
    truco.etapa_atual = "JC2"

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

    return resposta


def TRUCO(truco, conteudo, tipo_mensagem, resposta):
    aceitar_truco = input(
        "Cliente pediu TRUCO\n1 - Aceitar\n2 - Rejeitar\n"
    )

    tipo, mensagem = resposta.split("|")
    print(resposta)

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
            f"Servidor = {truco.placar[truco.servidor.nome]}\n" + \
            f"Cliente  = {truco.placar[truco.cliente.nome]}\n" + \
            "Começando nova rodada\n"

        resposta += placar
        print(placar)

        resposta = truco.proxima_rodada(resposta)

    return resposta


def RTRUCO(truco, conteudo, tipo_mensagem, resposta):
    aceitar_truco = conteudo

    # TRUCO aceito, joga carta
    if aceitar_truco == "1":
        truco.pontos_rodada = 2

        # Reenvia mesma mensagem após confirmação
        truco_mensagem = "TRUCO aceito\nA rodada agora vale 2 pontos\n"
        print(truco_mensagem)

        if truco.etapa_atual == "JC1":
            resposta = JC1(truco, conteudo, tipo_mensagem, resposta)
        elif truco.etapa_atual == "JC2":
            resposta = JC2(truco, conteudo, tipo_mensagem, resposta)

        tipo, mensagem = resposta.split("|")
        resposta = f"{tipo}|{truco_mensagem}{mensagem}"
    # TRUCO aceito, vai para próxima rodada
    else:
        resposta = f"TRUCO rejeitado\nPonto para servidor\n"
        print(resposta)

        # Atualiza placar
        truco.pontuacao_rodada[truco.servidor.nome] += 1

        # Vai para próxima rodada
        resposta = truco.proxima_rodada(resposta)

    return resposta
