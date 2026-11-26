import os
from http.server import ThreadingHTTPServer
from config import Config
from router import AppRequestHandler, DIRETORIO_FRONTEND

def iniciar():
    os.makedirs(DIRETORIO_FRONTEND, exist_ok=True)
    servidor = ThreadingHTTPServer((Config.APP_HOST, Config.APP_PORT), AppRequestHandler)
    print(f"🚀 Servidor ativo em http://localhost:{Config.APP_PORT}")
    print(f"📂 Servindo PWA de: {DIRETORIO_FRONTEND}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando servidor...")
        servidor.server_close()

if __name__ == "__main__":
    iniciar()
