"""Classe Orientacao: guarda um registro da base de conhecimento e o exibe na tela."""

AVISO = "este assistente NÃO é um canal oficial."


class Orientacao:
    """Representa uma orientação (um dicionário do JSON)."""

    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        """Mostra a orientação completa, com fonte, data e aviso (transparência)."""
        print(f"\n>> {self.titulo}  [{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        for documento in self.documentos:
            print(f"  - {documento}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(f"Aviso: {AVISO}")

    def __str__(self):
        return f"[{self.id}] {self.titulo}"
