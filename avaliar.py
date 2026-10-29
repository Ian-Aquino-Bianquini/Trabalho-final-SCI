"""Avaliação separada do treino. Execute: python avaliar.py"""

import json
from collections import Counter

from classificador import PASTA, carregar_modelo, ler_dados


def avaliar():
    modelo = carregar_modelo()
    testes = ler_dados(PASTA / "dados" / "teste.csv")
    treino = ler_dados(PASTA / "dados" / "treino.csv")
    assert not ({d["texto"] for d in treino} & {d["texto"] for d in testes}), "Há textos repetidos entre treino e teste."
    resultados = []
    acertos_categoria = Counter()
    totais_categoria = Counter()
    for caso in testes:
        previsao = modelo.classificar(caso["texto"])["categoria"]
        acerto = previsao == caso["categoria"]
        totais_categoria[caso["categoria"]] += 1
        acertos_categoria[caso["categoria"]] += acerto
        resultados.append({**caso, "previsao": previsao, "acerto": acerto})
    acertos = sum(r["acerto"] for r in resultados)
    relatorio = {
        "treino": len(treino), "teste": len(testes), "acertos": acertos,
        "acuracia": acertos / len(testes),
        "por_categoria": {c: {"acertos": acertos_categoria[c], "total": n} for c, n in totais_categoria.items()},
        "casos": resultados,
    }
    destino = PASTA / "resultados.json"
    destino.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{acertos}/{len(testes)} acertos ({relatorio['acuracia']:.1%}). Base fictícia e pequena.")
    for categoria, total in totais_categoria.items():
        print(f"{categoria}: {acertos_categoria[categoria]}/{total}")
    return relatorio


if __name__ == "__main__":
    avaliar()
