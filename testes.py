import unittest
import json
import threading
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from classificador import Classificador, carregar_modelo, palavras
from app import Atendimento


class TesteClassificador(unittest.TestCase):
    def setUp(self):
        self.modelo = carregar_modelo()

    def test_normaliza_acentos(self):
        self.assertEqual(palavras("ELÉTRICA, elétrica!"), ["eletrica", "eletrica"])

    def test_termos_desconhecidos_exigem_revisao(self):
        for texto in ["", "xyzabc", "o a de"]:
            self.assertEqual(self.modelo.classificar(texto)["categoria"], "revisao")

    def test_base_vazia(self):
        with self.assertRaises(ValueError):
            Classificador([])

    def test_encaminhamentos(self):
        for texto, categoria in [("torneira vazando", "hidraulica"), ("computador sem internet", "informatica"), ("tomada com faísca", "eletrica"), ("porta quebrada", "estrutura")]:
            with self.subTest(texto=texto):
                self.assertEqual(self.modelo.classificar(texto)["categoria"], categoria)


class TesteAplicacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = HTTPServer(("127.0.0.1", 0), Atendimento)
        cls.thread = threading.Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.servidor.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.servidor.server_close()
        cls.thread.join()

    def enviar(self, texto):
        return Request(self.url + "/classificar", json.dumps({"texto": texto}).encode(), {"Content-Type": "application/json"})

    def test_pagina_e_consulta(self):
        with urlopen(self.url) as resposta:
            self.assertIn('Sugerir setor', resposta.read().decode())
        with urlopen(self.enviar("A torneira está vazando")) as resposta:
            self.assertEqual(json.load(resposta)["categoria"], "hidraulica")

    def test_entrada_invalida(self):
        for texto in ["", 12, "x" * 2001]:
            with self.subTest(texto=str(texto)[:20]):
                with self.assertRaises(HTTPError) as erro:
                    urlopen(self.enviar(texto))
                self.assertEqual(erro.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
