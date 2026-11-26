import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "backend"))
from services import MenuService

class TestMenuService(unittest.TestCase):
    def test_construir_arvore_agrupa_sistemas_e_menus_sem_duplicar(self):
        dados_simulados = [
            {
                "idsistema": 7, "nomesistema": "Segurança", "sigla_sistema": "SEGURA", "url_sistema": "http://localhost",
                "idmodulomenu": 8, "menu": "Cadastros", "urlmenu": "0",
                "idtransacoes": 15, "transacao": "Sistemas", "urltransacao": "/sistemas",
                "idsubtransacao": None, "subtransacao": None
            },
            {
                "idsistema": 7, "nomesistema": "Segurança", "sigla_sistema": "SEGURA", "url_sistema": "http://localhost",
                "idmodulomenu": 8, "menu": "Cadastros", "urlmenu": "0",
                "idtransacoes": 16, "transacao": "Menus", "urltransacao": "/menus",
                "idsubtransacao": 1, "subtransacao": "Incluir Menu"
            }
        ]

        arvore = MenuService.construir_arvore_menus(dados_simulados)

        self.assertEqual(len(arvore), 1)
        self.assertEqual(arvore[0]["nome"], "Segurança")
        self.assertEqual(len(arvore[0]["menus"]), 1)
        self.assertEqual(len(arvore[0]["menus"][0]["transacoes"]), 2)
        self.assertEqual(arvore[0]["menus"][0]["transacoes"][1]["subtransacoes"][0]["nome"], "Incluir Menu")

    def test_usuario_vazio_dispara_erro(self):
        with self.assertRaises(ValueError):
            MenuService.obter_menus_por_usuario("   ")

if __name__ == "__main__":
    unittest.main()
