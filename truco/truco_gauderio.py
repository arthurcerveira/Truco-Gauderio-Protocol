from .baralho import Baralho, dar_as_cartas

MAXIMO_PONTOS = 4


class Truco(object):
    def __init__(self):
        # Atributos do jogo
        self.placar = dict()

        # Atributos para rodada
        self.servidor = None  # Servidor e cliente são da classe Jogador
        self.cliente = None

        # Mão é o jogador que começou a rodada
        self.mao = None

        # Número de pontos será alterado quando jogador pede Truco
        self.pontos_rodada = int()

        # Outros atributos tem servidor e cliente como chave para valores
        self.pontuacao_rodada = dict()
        self.cartas_na_mesa = dict()

        # Metadados
        self.etapa_atual = str()

    def inicializa_rodada(self, mao=None):
        # Pontos da rodada é 1 por padrão
        self.pontos_rodada = 1

        # Cria baralho
        baralho = Baralho()
        baralho.embaralhar()

        # Dá as cartas
        cartas_servidor, cartas_cliente = dar_as_cartas(baralho)

        # Cria jogadores
        self.servidor = Jogador(cartas_servidor, "Servidor")
        self.cliente = Jogador(cartas_cliente, "Cliente")

        # Define o mão da rodada
        if mao is not None:
            self.mao = mao
        else:
            # Mão é sempre o inverso do jogador atual
            self.mao = "Cliente" if self.mao == "Servidor" else "Servidor"

        # Inicializa pontuação da rodada
        self.pontuacao_rodada = {
            self.servidor.nome: 0,
            self.cliente.nome: 0
        }

    def cartas_disponiveis(self):
        cartas_disponiveis = self.servidor.cartas_disponiveis
        cartas_disponiveis += self.cliente.cartas_disponiveis

        return True if cartas_disponiveis > 0 else False

    def maior_carta(self, carta1, carta2, jogador):
        # Verifica qual carta é maior
        if carta1 > carta2:
            resposta = f"{carta1} é maior que {carta2}\n"

            # Atualiza pontuação da rodada
            self.pontuacao_rodada[self.servidor.nome] += 1

            proximo_jogador = self.servidor.nome

        elif carta2 > carta1:
            resposta = f"{carta2} é maior que {carta1}\n"

            # Atualiza pontuação da rodada
            self.pontuacao_rodada[self.cliente.nome] += 1

            proximo_jogador = self.cliente.nome

        else:
            resposta = "As duas cartas tem o mesmo valor\n"

            proximo_jogador = jogador

        return resposta, proximo_jogador

    def ganhou_rodada(self):
        pontos = self.pontuacao_rodada.values()

        if 2 in pontos:
            if self.pontuacao_rodada[self.servidor.nome] == 2:
                ganhador = self.servidor.nome
            else:
                ganhador = self.cliente.nome

            return ganhador

        return None

    def fim_rodada(self, resposta):
        ganhador = self.ganhou_rodada()

        if ganhador is not None:
            # Atualiza placar com ganhador
            ganhador_rodada = f"Fim da rodada. Ponto para {ganhador}\n"
            print(ganhador_rodada)
            resposta += ganhador_rodada

            self.placar[ganhador] += self.pontos_rodada

        # Verifica se rodada acabou (número de cartas)
        elif self.cartas_disponiveis() is False:
            # Se nº de cartas = 0 e pontuação < 2, vitória da mão
            ganhador = self.mao

            ganhador_rodada = f"Empate. Ponto para {ganhador}\n"

            print(ganhador_rodada)
            resposta += ganhador_rodada

            # Atualiza placar com ganhador
            self.placar[ganhador] += self.pontos_rodada

        else:
            # Rodada não acabou
            return False

        return resposta

    def proxima_jogada(self, resposta, proximo_jogador):
        # Servidor joga a próxima carta
        if proximo_jogador == self.servidor.nome:
            self.etapa_atual = "JC1"

            # Escolhe carta
            carta = self.servidor.escolhe_carta()

            self.cartas_na_mesa[self.servidor.nome] = carta

            # Resposta do cliente inicia com chave JS1
            resposta = "JS1|" + resposta

            # Envia carta na mesa
            resposta += f"Servidor jogou a carta {carta}\n"

        # Cliente joga a próxima carta
        else:
            self.etapa_atual = "JC2"
            resposta = "JS2|" + resposta

        # Envia para cliente suas cartas
        resposta += mostrar_cartas(self.cliente.cartas)
        resposta += "Escolha sua carta:"

        return resposta

    def proxima_rodada(self, resposta):
        ganhador = self.ganhou_jogo()

        if ganhador is not None:
            resposta = "FJ|" + resposta
            fim_de_jogo = f"Fim de jogo\n{ganhador} venceu\n"
            print(fim_de_jogo)
            resposta += fim_de_jogo
        else:
            resposta += "Começando nova rodada\n"
            self.inicializa_rodada()
            resposta = self.proxima_jogada(resposta, self.mao)

        return resposta

    def ganhou_jogo(self):
        if self.placar["Servidor"] >= MAXIMO_PONTOS:
            return "Servidor"

        if self.placar["Cliente"] >= MAXIMO_PONTOS:
            return "Cliente"

        return None


def mostrar_cartas(cartas):
    cartas_texto = str()

    for indice in cartas:
        carta = cartas[indice]

        cartas_texto += f"{indice} - {carta}\n"

    return cartas_texto


class Jogador(object):
    def __init__(self, cartas, nome):
        self.cartas = cartas
        self.nome = nome

    @property
    def cartas_disponiveis(self):
        opcoes = {indice for indice in self.cartas
                  if self.cartas[indice] != ""}
        return len(opcoes)

    def escolhe_carta(self):
        cartas = mostrar_cartas(self.cartas)
        print(cartas)

        # Obtem opções de cartas
        opcoes = {str(indice) for indice in self.cartas
                  if self.cartas[indice] != ""}

        indice = input("Escolha uma carta: ")

        # Jogador pede TRUCO antes de escolher a carta
        if indice == "TRUCO":
            return "TRUCO"

        while indice not in opcoes:
            indice = input("Valor inválido. Escolha uma carta: ")

            if indice == "TRUCO":
                return "TRUCO"

        carta = self.cartas[int(indice)]

        # Remove opção de carta
        self.cartas[int(indice)] = ""

        return carta

    def __str__(self):
        return self.name
