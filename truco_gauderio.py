from itertools import product
from random import shuffle

NAIPES = ('ouros', 'espadas', 'copas', 'bastos')
NUMEROS = list(range(1, 13))

# Truco gaudério não usa cartas 8 e 9
NUMEROS.remove(8)
NUMEROS.remove(9)

REPRESENTACAO = {
    1: 'Ás',
    10: 'Sota',
    11: 'Cavalo',
    12: 'Rei'
}


class Carta(object):
    def __init__(self,  naipe, numero):
        self.naipe = naipe
        self.numero = numero

    def __str__(self):
        representacao = REPRESENTACAO.get(self.numero)
        if representacao is None:
            representacao = self.numero

        return f"{representacao} de {self.naipe}"


class Baralho(object):
    def __init__(self):
        self.cartas = list()
        self.criar_baralho()

    def criar_baralho(self):
        # Remove cartas antes de adicionar novas
        self.cartas.clear()

        for naipe, numero in product(NAIPES, NUMEROS):
            carta = Carta(naipe, numero)

            self.cartas.append(carta)

    def embaralhar(self):
        shuffle(self.cartas)

    def tirar_carta(self):
        return self.cartas.pop()


def dar_as_cartas(baralho):
    # 3 cartas para cada jogador
    jogador_1 = list()
    jogador_2 = list()

    for _ in range(3):
        carta = baralho.tirar_carta()
        jogador_1.append(carta)

        carta = baralho.tirar_carta()
        jogador_2.append(carta)

    return jogador_1, jogador_2


if __name__ == '__main__':
    baralho = Baralho()
    baralho.embaralhar()

    for i in range(5):
        carta = baralho.tirar_carta()

        print(str(carta))
