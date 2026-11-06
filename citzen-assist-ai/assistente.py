"""Classe Assistente: conversa com o cidadão, guarda o histórico e calcula indicadores."""

import csv
import json
import os
import time
from datetime import datetime

from base_conhecimento import BaseConhecimento, normalizar

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_segundos"]

# Mensagens com esses trechos recebem acolhimento e o contato de apoio emocional.
# O texto digitado NÃO é gravado no histórico (é sensível).
SINAIS_SOFRIMENTO = ["suicid", "me matar", "quero morrer", "pensando em morrer",
                     "nao aguento mais", "acabar com minha vida", "tirar minha vida",
                     "me machucar", "automutilacao", "quero sumir"]
PERGUNTA_SENSIVEL = "[mensagem sensível: texto não registrado]"
CATEGORIA_APOIO = "Apoio Emocional"


# ---------------------------------------------------------------- entradas
def entrada(mensagem):
    """input() que não quebra se a entrada terminar (devolve None)."""
    try:
        return input(mensagem)
    except EOFError:
        return None


def ler_numero(mensagem, minimo, maximo):
    """Pede um número entre minimo e maximo. Letras, vazio e fora da faixa
    nunca encerram o programa: a pergunta é repetida. Devolve None se a entrada acabar."""
    while True:
        texto = entrada(mensagem)
        if texto is None:
            return None
        try:
            numero = int(texto.strip())
            if minimo <= numero <= maximo:
                return numero
        except ValueError:
            pass
        print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")


def ler_sim_nao(mensagem):
    """Pede s/n. Qualquer outra resposta repete a pergunta."""
    while True:
        texto = entrada(mensagem)
        if texto is None:
            return False
        texto = texto.strip().lower()
        if texto in ("s", "sim"):
            return True
        if texto in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite s para sim ou n para não.")


# ---------------------------------------------------------------- classe
class Assistente:
    """Quem conversa com o cidadão."""

    def __init__(self, nome, base, pasta_dados="data"):
        self.nome = nome
        self.base = base                      # objeto BaseConhecimento (composição)
        self.pasta_dados = pasta_dados
        self.caminho_historico = os.path.join(pasta_dados, "historico.json")
        self.caminho_csv = os.path.join(pasta_dados, "atendimentos.csv")
        self.caminho_notas = os.path.join(pasta_dados, "avaliacoes.json")
        self.historico = self._ler_lista(self.caminho_historico)
        self.notas = self._ler_lista(self.caminho_notas)

    # ---------- arquivos
    def _ler_lista(self, caminho):
        """Lê uma lista de dicionários de um JSON. Ausente ou corrompido => lista vazia."""
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, OSError):
            print(f"Aviso: '{caminho}' está ilegível. Começando com lista vazia.")
            return []
        if not isinstance(dados, list):
            return []
        return [item for item in dados if isinstance(item, dict)]

    def _salvar_lista(self, lista, caminho):
        try:
            os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(lista, arquivo, ensure_ascii=False, indent=2)
            return True
        except OSError:
            print(f"Aviso: não foi possível salvar '{caminho}'.")
            return False

    # ---------- dados pessoais
    @staticmethod
    def tem_dado_pessoal(texto):
        """8 ou mais dígitos (CPF, telefone...) ou '@' (e-mail)."""
        digitos = sum(1 for letra in texto if letra.isdigit())
        return digitos >= 8 or "@" in texto

    @staticmethod
    def tem_sinal_sofrimento(texto):
        texto_norm = normalizar(texto)
        return any(sinal in texto_norm for sinal in SINAIS_SOFRIMENTO)

    # ---------- registro
    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo_segundos):
        """Guarda um atendimento em data/historico.json. Recusa dados pessoais."""
        if self.tem_dado_pessoal(pergunta):
            return False
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,                 # "pergunta" ou "categoria"
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,                 # True, False ou None (não perguntado)
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos,
        }
        self.historico.append(atendimento)
        self._salvar_lista(self.historico, self.caminho_historico)
        return True

    # ---------- atendimento por texto livre
    def perguntar(self):
        while True:                           # cada volta = um novo atendimento
            inicio = time.time()
            tentativas = 0
            ultima = ""
            encontrou = False
            id_final = None
            ajudou = False
            tempo = None
            finalizou = False

            while not finalizou:
                texto = entrada("\nDigite sua dúvida (0 para voltar): ")
                texto = "0" if texto is None else texto.strip()

                if texto == "0":
                    if tentativas > 0:        # só registra se houve atendimento
                        if tempo is None:
                            tempo = round(time.time() - inicio, 1)
                        self.registrar("pergunta", ultima, id_final, encontrou,
                                       ajudou, tentativas, tempo)
                    return
                if texto == "":
                    print("Você não digitou nada. Escreva sua dúvida ou digite 0 para voltar.")
                    continue
                if self.tem_dado_pessoal(texto):
                    print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                    continue                  # não conta tentativa e não é registrado

                tentativas += 1

                if self.tem_sinal_sofrimento(texto):
                    self._acolher()
                    self.registrar("pergunta", PERGUNTA_SENSIVEL, None, True, None,
                                   tentativas, round(time.time() - inicio, 1))
                    finalizou = True
                    continue

                ultima = texto
                resultados = self.base.buscar(texto)
                nivel = BaseConhecimento.nivel_confianca(resultados[0][0]) if resultados else None
                if nivel is None:
                    print("\nNão encontrei uma orientação para essa dúvida.")
                    print("Tente outras palavras (ex.: denunciar, nome social, PrEP, casamento)")
                    print("ou use a opção de navegar por categorias:")
                    print("  " + ", ".join(self.base.categorias()))
                    continue

                tempo = round(time.time() - inicio, 1)
                encontrou = True
                pontos, melhor = resultados[0]
                id_final = melhor.id
                print(f"\nConfiança da resposta: {nivel} ({pontos} pontos)")
                melhor.exibir()

                alternativas = [o for _, o in resultados[1:3]]
                if alternativas:
                    print("\nOutras orientações relacionadas:")
                    for i, orientacao in enumerate(alternativas, start=1):
                        print(f"  {i}. {orientacao.titulo}")

                ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                if not ajudou and alternativas:
                    escolha = ler_numero("Quer ver uma das orientações relacionadas? "
                                         "Digite o número (0 para não): ", 0, len(alternativas))
                    if escolha:
                        outra = alternativas[escolha - 1]
                        outra.exibir()
                        id_final = outra.id
                        ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")

                if ajudou:
                    self.registrar("pergunta", ultima, id_final, True, True, tentativas, tempo)
                    finalizou = True
                elif ler_sim_nao("Quer reescrever a pergunta? (s/n): "):
                    continue                  # mesma sessão: mais uma tentativa
                else:
                    self.registrar("pergunta", ultima, id_final, True, False, tentativas, tempo)
                    finalizou = True

    def _acolher(self):
        """Mensagem de cuidado + contato de apoio emocional da base."""
        print("\nSinto muito que você esteja passando por um momento tão difícil.")
        print("Você não precisa enfrentar isso sozinha(o). Este serviço pode ajudar agora:")
        apoio = self.base.por_categoria(CATEGORIA_APOIO)
        if apoio:
            apoio[0].exibir()
        else:
            print("Procure um serviço de saúde ou de urgência perto de você.")

    # ---------- navegação por categorias
    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis.")
            return
        while True:
            print("\n--- Categorias ---")
            for i, categoria in enumerate(categorias, start=1):
                print(f"  {i}. {categoria}")
            print("  0. Voltar")
            escolha = ler_numero("Escolha uma categoria: ", 0, len(categorias))
            if not escolha:
                return
            self._navegar_orientacoes(categorias[escolha - 1])

    def _navegar_orientacoes(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            print(f"\n--- {categoria} ---")
            for i, orientacao in enumerate(orientacoes, start=1):
                print(f"  {i}. {orientacao.titulo}")
            print("  0. Voltar")
            inicio = time.time()
            escolha = ler_numero("Escolha uma orientação: ", 0, len(orientacoes))
            if not escolha:
                return
            tempo = round(time.time() - inicio, 1)
            orientacao = orientacoes[escolha - 1]
            orientacao.exibir()
            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("categoria", f"Categoria: {categoria}", orientacao.id,
                           True, ajudou, 1, tempo)

    # ---------- indicadores
    def indicadores(self):
        """Calcula os indicadores a partir do histórico. Devolve um dicionário."""
        total = len(self.historico)
        if total == 0:
            return None

        def media(valores):
            return round(sum(valores) / len(valores), 1) if valores else None

        encontrados = [a for a in self.historico if a.get("encontrou")]
        avaliados = [a for a in self.historico if a.get("ajudou") is not None]
        ajudaram = [a for a in avaliados if a.get("ajudou")]
        tempos = [a.get("tempo_segundos", 0) for a in encontrados]
        tentativas = [a.get("tentativas", 1) for a in self.historico]
        notas = [n.get("nota") for n in self.notas if isinstance(n.get("nota"), int)]

        sem_solucao = []
        for a in self.historico:
            if (not a.get("encontrou") or a.get("ajudou") is False) \
                    and a.get("pergunta") != PERGUNTA_SENSIVEL \
                    and a.get("pergunta") not in sem_solucao:
                sem_solucao.append(a.get("pergunta"))

        return {
            "total": total,
            "encontrada_pct": round(100 * len(encontrados) / total, 1),
            "acerto_pct": round(100 * len(ajudaram) / len(avaliados), 1) if avaliados else None,
            "tempo_medio": media(tempos),
            "tentativas_media": media(tentativas),
            "facilidade_media": media(notas),
            "avaliacoes": len(notas),
            "sem_solucao": sem_solucao,
        }

    def mostrar_indicadores(self):
        dados = self.indicadores()
        print("\n===== Indicadores =====")
        if dados is None:
            print("Ainda não há atendimentos registrados.")
            return

        def formatar(valor, unidade=""):
            return "sem dados" if valor is None else f"{valor}{unidade}"

        print(f"Atendimentos registrados:        {dados['total']}")
        print(f"Resposta encontrada:             {formatar(dados['encontrada_pct'], '%')}")
        print(f"Taxa de acerto (ajudou):         {formatar(dados['acerto_pct'], '%')}")
        print(f"Tempo médio para encontrar:      {formatar(dados['tempo_medio'], ' s')}")
        print(f"Tentativas por atendimento:      {formatar(dados['tentativas_media'])}")
        print(f"Facilidade de uso (1 a 5):       {formatar(dados['facilidade_media'])}"
              f" ({dados['avaliacoes']} avaliações)")
        print("Dúvidas sem solução:")
        if dados["sem_solucao"]:
            for pergunta in dados["sem_solucao"]:
                print(f"  - {pergunta}")
        else:
            print("  (nenhuma)")

    # ---------- CSV
    def exportar_csv(self):
        """Exporta o histórico para data/atendimentos.csv com csv.DictWriter."""
        if not self.historico:
            print("Nenhum atendimento para exportar ainda.")
            return False
        try:
            os.makedirs(os.path.dirname(self.caminho_csv) or ".", exist_ok=True)
            with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV, extrasaction="ignore")
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow(atendimento)
        except OSError:
            print("Aviso: não foi possível gravar o CSV (o arquivo pode estar aberto em outro programa).")
            return False
        print(f"{len(self.historico)} atendimentos exportados para {self.caminho_csv}")
        return True

    # ---------- menu principal
    def iniciar(self):
        print(f"\n=== {self.nome} ===")
        print("Orientações com fonte oficial para pessoas LGBTQIA+: saúde, direitos, documentos e denúncia.")
        print("Aviso: este assistente NÃO é um canal oficial.")
        print("Privacidade: não digite nome, CPF, telefone ou e-mail. Nada disso é pedido nem guardado.")
        while True:
            print("\n--- Menu ---")
            print("  1. Digitar minha dúvida")
            print("  2. Navegar por categorias")
            print("  3. Ver indicadores")
            print("  4. Exportar atendimentos para CSV")
            print("  0. Sair")
            opcao = ler_numero("Escolha uma opção: ", 0, 4)
            if opcao == 1:
                self.perguntar()
            elif opcao == 2:
                self.navegar()
            elif opcao == 3:
                self.mostrar_indicadores()
            elif opcao == 4:
                self.exportar_csv()
            else:                             # 0 ou entrada encerrada
                self.sair()
                return

    def sair(self):
        nota = ler_numero("\nAntes de sair, dê uma nota de facilidade de uso (1 a 5): ", 1, 5)
        if nota is not None:
            self.notas.append({"data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               "nota": nota})
            self._salvar_lista(self.notas, self.caminho_notas)
        print("Obrigado por usar o Cinclu. Cuide-se!")
