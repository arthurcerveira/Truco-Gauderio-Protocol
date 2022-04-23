from truco_gauderio import Baralho, dar_as_cartas


class Jogador(object):
    def __init__(self, cartas):
        self.cartas = cartas

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


if __name__ == '__main__':
    # Inicializa o baralho
    baralho = Baralho()
    baralho.embaralhar()

    # Pega as cartas
    cartas_j1, cartas_j2 = dar_as_cartas(baralho)

    # Inicializa jogadores
    jogador1 = Jogador(cartas_j1)
    jogador2 = Jogador(cartas_j2)

    # Jogador 1 escolhe uma carta
    while True:
        print("Jogador 1")
        carta_j1 = jogador1.escolhe_carta()
        print(f"Carta escolhida: {carta_j1}")

        print("\nJogador 2")
        carta_j2 = jogador2.escolhe_carta()
        print(f"Carta escolhida: {carta_j2}")
