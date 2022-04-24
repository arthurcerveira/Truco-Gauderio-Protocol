J1 = 1
J2 = 2


class Truco(object):
    def __init__(self):
        # Atributos para rodada
        self.servidor = None  # Servidor e cliente são da classe Jogador
        self.cliente = None

        # Outros atributos tem servidor e cliente como chave para valores
        self.pontuacao_rodada = dict()
        self.cartas_na_mesa = dict()


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
        opcoes = {indice for indice in self.cartas
                  if self.cartas[indice] != ""}

        indice = int(input("Escolha uma carta: "))
        while indice not in opcoes:
            indice = int(input("Valor inválido. Escolha uma carta: "))

        carta = self.cartas[indice]

        # Remove opção de carta
        self.cartas[indice] = ""

        return carta

    def __str__(self):
        return self.name
