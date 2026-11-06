"""Cinclu (Cidade Inclusiva): assistente de orientação para pessoas LGBTQIA+.
Execute com: python main.py"""

import os

from base_conhecimento import BaseConhecimento
from assistente import Assistente

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA, "data")


def main():
    base = BaseConhecimento(os.path.join(PASTA_DADOS, "base_conhecimento.json"))
    base.carregar()                 # lê o JSON e cria os objetos Orientacao
    if not base.orientacoes:
        print("Não foi possível carregar a base de conhecimento.")
        print("Verifique se data/base_conhecimento.json existe e está correto.")
        return

    assistente = Assistente("Cinclu - Cidade Inclusiva", base, PASTA_DADOS)
    try:
        assistente.iniciar()
    except KeyboardInterrupt:
        print("\nAtendimento encerrado. Cuide-se!")


if __name__ == "__main__":
    main()
