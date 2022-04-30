# Truco Gaudério Protocol

Implementação de um protocolo de rede da camada aplicação para jogar Truco Gaudério através de uma conexão TCP entre cliente e servidor.

## Instruções

Para executar os códigos do cliente e servidor é necessário apenas duas máquinas com Python >=3.8.

Para executar localmente simulando duas máquina conectadas, pode se utilizar um container Docker para rodar o servidor.

```bash
$ docker build -t tgp .
$ docker run --name servidor-tgp -i tgp
Host: xxx.xx.x.x
```

Quando executado, o servidor vai indicar o seu endereço para a conexão, que deve ser redefinido dentro do script `cliente.py`.

```python
from socket import *


host = 'xxx.xx.x.x'
port = 6050
```

Esse cliente pode ser então rodado localmente.

```bash
$ python cliente.py
Digite IJ para inciar o jogo de Truco Gaudério:
```
