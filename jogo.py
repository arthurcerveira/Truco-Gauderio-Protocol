from truco_gauderio import Baralho, dar_as_cartas


J1 = 1
J2 = 2

PROXIMO_JOGADOR = {
    J1: J2,
    J2: J1
}


class Jogador(object):
    def __init__(self, cartas):
        self.cartas = cartas

    @property
    def cartas_disponiveis(self):
        opcoes = {indice for indice in self.cartas
                  if self.cartas[indice] != ""}
        return len(opcoes)

    def mostrar_cartas(self):
        cartas = str()

        for indice in self.cartas:
            carta = self.cartas[indice]

            cartas += f"{indice} - {carta}\n"

        return cartas

    def escolhe_carta(self):
        cartas = self.mostrar_cartas()
        print(cartas)

        # Obtem opções de cartas
        opcoes = {indice for indice in self.cartas
                  if self.cartas[indice] != ""}

        indice = int(input("Escolha uma carta: "))
        while indice not in opcoes:
            indice = int(input("Valor inválido. Escolha uma carta: "))

        carta = self.cartas[indice]

        # Remove opção de carta
        self.cartas[indice] = ""

        return carta


class Truco(object):
    def __init__(self):
        self.baralho = Baralho()
        self.jogadores = self.inicia_jogadores()
        self.pontuacao = {
            J1: 0,
            J2: 0
        }

    def inicia_jogadores(self):
        self.baralho.embaralhar()

        # Pega as cartas
        cartas_j1, cartas_j2 = dar_as_cartas(self.baralho)

        # Inicializa jogadores
        jogadores = dict()

        jogadores[J1] = Jogador(cartas_j1)
        jogadores[J2] = Jogador(cartas_j2)

        return jogadores

    def rodada(self):
        jogador = J1

        pontuacao_rodada = {
            J1: 0,
            J2: 0
        }

        cartas_em_jogo = {
            J1: None,
            J2: None
        }

        while True:
            print(f"Jogador {jogador}")
            cartas_em_jogo[jogador] = self.jogadores[jogador].escolhe_carta()
            print(f"Carta escolhida: {cartas_em_jogo[jogador]}\n")

            # Próximo jogador é sempre o contrario do jogador atual
            jogador = PROXIMO_JOGADOR[jogador]
            print(f"\nJogador {jogador}")
            cartas_em_jogo[jogador] = self.jogadores[jogador].escolhe_carta()

            print(f"Carta escolhida: {cartas_em_jogo[jogador]}\n")

            # Carta do J1 é maior
            if cartas_em_jogo[J1] > cartas_em_jogo[J2]:
                print(f"{cartas_em_jogo[J1]} é maior que {cartas_em_jogo[J2]}")
                pontuacao_rodada[J1] += 1
                jogador = J1

            elif cartas_em_jogo[J2] > cartas_em_jogo[J1]:
                print(f"{cartas_em_jogo[J2]} é maior que {cartas_em_jogo[J1]}")
                pontuacao_rodada[J2] += 1
                jogador = J2

            else:
                print("As duas cartas tem o mesmo valor\n")

            print(f"Pontuação da rodada:\n{pontuacao_rodada}\n")


if __name__ == '__main__':
    # Inicializa o baralho
    truco = Truco()
    truco.inicia_jogadores()

    truco.rodada()
