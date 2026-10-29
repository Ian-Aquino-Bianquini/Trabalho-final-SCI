"""Interface local. Execute: python app.py"""

import json
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from classificador import PASTA, carregar_modelo

MODELO = carregar_modelo()


class Atendimento(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        pagina = (PASTA / "pagina.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(pagina)

    def do_POST(self):
        if self.path != "/classificar":
            self.send_error(404)
            return
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if not 0 < tamanho <= 10000:
                raise ValueError("Informe uma descrição com até 2.000 caracteres.")
            entrada = json.loads(self.rfile.read(tamanho))
            texto = entrada.get("texto", "")
            if not isinstance(texto, str) or not texto.strip() or len(texto) > 2000:
                raise ValueError("Informe uma descrição com até 2.000 caracteres.")
            resultado = MODELO.classificar(texto)
            status = 200
        except (ValueError, TypeError, AttributeError):
            resultado = {"erro": "Informe uma descrição válida com até 2.000 caracteres."}
            status = 400
        resposta = json.dumps(resultado, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(resposta)


if __name__ == "__main__":
    endereco = "http://127.0.0.1:8000"
    servidor = HTTPServer(("127.0.0.1", 8000), Atendimento)
    print(f"Triagem disponível em {endereco}. Para encerrar, pressione Ctrl+C.")
    webbrowser.open(endereco)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nAplicação encerrada.")
    finally:
        servidor.server_close()
