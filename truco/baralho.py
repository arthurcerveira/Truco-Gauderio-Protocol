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

# Força das manilhas do jogo
MANILHAS = {
    "Ás de espadas": 14,
    "Ás de bastos": 13,
    "7 de espadas": 12,
    "7 de ouros": 11,
}

# Rankign de força das cartas
RANKING = {
    4: 1,
    5: 2,
    6: 3,
    7: 4,
    10: 5,
    11: 6,
    12: 7,
    1: 8,
    2: 9,
    3: 10,
}


class Carta(object):
    def __init__(self,  naipe, numero):
        self.naipe = naipe
        self.numero = numero
        self.forca = self.forca_da_carta()

    def __str__(self):
        representacao = REPRESENTACAO.get(self.numero)
        if representacao is None:
            representacao = self.numero

        return f"{representacao} de {self.naipe}"

    def forca_da_carta(self):
        # Verifica se é manilha
        representacao = self.__str__()

        if representacao in MANILHAS:
            return MANILHAS[representacao]

        return RANKING[self.numero]

    def __gt__(self, outro):
        return self.forca > outro.forca


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
    jogador_1 = dict()
    jogador_2 = dict()

    for indice in range(1, 4):
        carta = baralho.tirar_carta()
        jogador_1[indice] = carta

        carta = baralho.tirar_carta()
        jogador_2[indice] = carta

    return jogador_1, jogador_2


if __name__ == '__main__':
    baralho = Baralho()
    baralho.embaralhar()

    for i in range(5):
        carta = baralho.tirar_carta()

        print(str(carta))
