import json
from datetime import date, datetime
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from services import MenuService

DIRETORIO_FRONTEND = str(Path(__file__).resolve().parents[1] / "frontend")

class JsonEncoderISO(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

class AppRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRETORIO_FRONTEND, **kwargs)

    def _responder_json(self, status: int, dados: dict | list):
        corpo = json.dumps(dados, cls=JsonEncoderISO, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _ler_json(self) -> dict:
        tamanho = int(self.headers.get("Content-Length", 0))
        if tamanho == 0:
            return {}
        return json.loads(self.rfile.read(tamanho).decode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        rota = parsed.path
        params = parse_qs(parsed.query)

        if not rota.startswith("/api/"):
            return super().do_GET()

        usuario = params.get("usuario", [""])[0]

        try:
            if rota == "/api/menus":
                menus = MenuService.obter_menus_por_usuario(usuario)
                return self._responder_json(200, menus)

            if rota == "/api/os/pendentes":
                pendentes = MenuService.obter_os_pendentes(usuario)
                return self._responder_json(200, pendentes)

            return self._responder_json(404, {"erro": "Rota não encontrada."})

        except ValueError as err:
            return self._responder_json(400, {"erro": str(err)})
        except Exception as err:
            print(f"[ERRO GET {rota}]: {err}")
            return self._responder_json(500, {"erro": "Erro interno no servidor."})

    def do_POST(self):
        rota = urlparse(self.path).path

        if rota == "/api/os/ciencia":
            try:
                body = self._ler_json()
                id_ciencia = int(body.get("idordemservicociencia", 0))
                usuario = str(body.get("usuario", ""))

                if MenuService.dar_ciencia_os(id_ciencia, usuario):
                    return self._responder_json(200, {"mensagem": "Ciência confirmada com sucesso."})
                return self._responder_json(404, {"erro": "OS não encontrada ou já aceita."})

            except ValueError as err:
                return self._responder_json(400, {"erro": str(err)})
            except Exception as err:
                print(f"[ERRO POST {rota}]: {err}")
                return self._responder_json(500, {"erro": "Erro interno no servidor."})

        return self._responder_json(404, {"erro": "Rota não encontrada."})
