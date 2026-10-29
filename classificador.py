"""Classificação de chamados por Naive Bayes multinomial, sem bibliotecas externas."""

import csv
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

PASTA = Path(__file__).resolve().parent
SETORES = {
    "eletrica": "Manutenção elétrica",
    "hidraulica": "Manutenção hidráulica",
    "informatica": "Suporte de informática",
    "estrutura": "Manutenção predial",
}
PALAVRAS_COMUNS = set("a o as os um uma de da do das dos e em no na nos nas para por com que esta está meu minha não nao ao se tem muito".split())


def palavras(texto):
    normalizado = unicodedata.normalize("NFKD", texto.lower())
    normalizado = "".join(letra for letra in normalizado if not unicodedata.combining(letra))
    return [p for p in re.findall(r"[a-z]+", normalizado) if p not in PALAVRAS_COMUNS and len(p) > 1]


def ler_dados(caminho):
    with Path(caminho).open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


class Classificador:
    def __init__(self, exemplos):
        self.documentos = Counter()
        self.contagens = defaultdict(Counter)
        self.vocabulario = set()
        for exemplo in exemplos:
            categoria = exemplo["categoria"]
            termos = palavras(exemplo["texto"])
            self.documentos[categoria] += 1
            self.contagens[categoria].update(termos)
            self.vocabulario.update(termos)
        if not self.documentos or not self.vocabulario:
            raise ValueError("A base de treinamento precisa conter textos e categorias.")
        self.totais = {c: sum(contagem.values()) for c, contagem in self.contagens.items()}
        self.total_documentos = sum(self.documentos.values())

    def classificar(self, texto):
        termos = Counter(p for p in palavras(texto) if p in self.vocabulario)
        if not termos:
            return {"categoria": "revisao", "setor": "Triagem manual", "motivo": "Não há termos conhecidos suficientes para sugerir um setor."}
        notas = {}
        for categoria, quantidade in self.documentos.items():
            nota = math.log(quantidade / self.total_documentos)
            denominador = self.totais[categoria] + len(self.vocabulario)
            for termo, frequencia in termos.items():
                nota += frequencia * math.log((self.contagens[categoria][termo] + 1) / denominador)
            notas[categoria] = nota
        categoria = max(notas, key=notas.get)
        conhecidos = ", ".join(sorted(termos))
        return {"categoria": categoria, "setor": SETORES[categoria], "motivo": f"Termos presentes na base: {conhecidos}. Conferir o encaminhamento."}


def carregar_modelo():
    return Classificador(ler_dados(PASTA / "dados" / "treino.csv"))
