"""Classe BaseConhecimento: lê o JSON, lista categorias e busca a melhor orientação."""

import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

CAMPOS = ["id", "categoria", "titulo", "palavras_chave", "resposta",
          "documentos", "onde", "fonte", "verificado_em"]

# Palavras comuns com 4+ letras que não ajudam a achar o assunto.
# Sem isso, "como" (que está em vários títulos) daria +1 ponto à toa.
IGNORAR_NO_TITULO = {"como", "para", "qual", "quais", "onde", "quando", "posso",
                     "pode", "fazer", "sobre", "minha", "meus", "minhas", "esse",
                     "essa", "isso", "quero", "preciso", "tenho", "estou"}

PONTOS_PALAVRA_CHAVE = 3
PONTOS_TITULO = 1
LIMITE_ALTA = 6
LIMITE_MEDIA = 3


def normalizar(texto):
    """Minúsculas, sem acentos e sem pontuação. Devolve o texto com espaço nas pontas."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()\"'/+":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    """Conjunto de todas as orientações."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []  # lista de objetos Orientacao

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao.
        Devolve True se carregou algo; nunca trava o programa."""
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Aviso: arquivo '{self.caminho}' não encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Aviso: arquivo '{self.caminho}' está corrompido.")
            return False
        except OSError:
            print(f"Aviso: não foi possível abrir '{self.caminho}'.")
            return False

        if not isinstance(dados, list):
            print("Aviso: a base de conhecimento deve ser uma lista de orientações.")
            return False

        for item in dados:
            if isinstance(item, dict) and all(campo in item for campo in CAMPOS):
                self.orientacoes.append(Orientacao(**{c: item[c] for c in CAMPOS}))
            else:
                print("Aviso: uma orientação incompleta foi ignorada.")
        return len(self.orientacoes) > 0

    def categorias(self):
        """Lista de categorias, sem repetir e na ordem em que aparecem."""
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        """Orientações de uma categoria."""
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """+3 por palavra-chave que aparece na pergunta;
        +1 por palavra da pergunta (4+ letras) que aparece no título."""
        pergunta_norm = normalizar(pergunta)
        pontos = 0
        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta_norm:
                pontos += PONTOS_PALAVRA_CHAVE
        titulo_norm = normalizar(orientacao.titulo)
        for palavra in set(pergunta_norm.split()):
            if (len(palavra) >= 4 and palavra not in IGNORAR_NO_TITULO
                    and f" {palavra} " in titulo_norm):
                pontos += PONTOS_TITULO
        return pontos

    def buscar(self, pergunta):
        """Devolve lista de tuplas (pontos, orientacao), da maior para a menor pontuação.
        Só entram orientações com pelo menos 1 ponto."""
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultados

    @staticmethod
    def nivel_confianca(pontos):
        """ALTA (6+), MÉDIA (3 a 5) ou None (menos de 3: 'não encontrei')."""
        if pontos >= LIMITE_ALTA:
            return "ALTA"
        if pontos >= LIMITE_MEDIA:
            return "MÉDIA"
        return None
