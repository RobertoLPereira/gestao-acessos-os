from repositories import AcessoRepository

class MenuService:
    @staticmethod
    def construir_arvore_menus(linhas_banco: list[dict]) -> list[dict]:
        """Transforma linhas planas da view PermissoesWs em árvore hierárquica."""
        sistemas = {}

        for row in linhas_banco:
            id_sis = row["idsistema"]
            if id_sis not in sistemas:
                sistemas[id_sis] = {
                    "id": id_sis,
                    "nome": row["nomesistema"],
                    "sigla": row["sigla_sistema"],
                    "url": row["url_sistema"],
                    "menus": {}
                }

            id_men = row["idmodulomenu"]
            if id_men not in sistemas[id_sis]["menus"]:
                sistemas[id_sis]["menus"][id_men] = {
                    "id": id_men,
                    "nome": row["menu"],
                    "url": row["urlmenu"],
                    "transacoes": {}
                }

            id_tra = row["idtransacoes"]
            if id_tra not in sistemas[id_sis]["menus"][id_men]["transacoes"]:
                sistemas[id_sis]["menus"][id_men]["transacoes"][id_tra] = {
                    "id": id_tra,
                    "nome": row["transacao"],
                    "url": row["urltransacao"],
                    "subtransacoes": []
                }

            if row.get("idsubtransacao") is not None:
                sistemas[id_sis]["menus"][id_men]["transacoes"][id_tra]["subtransacoes"].append({
                    "id": row["idsubtransacao"],
                    "nome": row["subtransacao"]
                })

        resultado = []
        for sis in sistemas.values():
            menus_lista = []
            for men in sis["menus"].values():
                men["transacoes"] = list(men["transacoes"].values())
                menus_lista.append(men)
            sis["menus"] = menus_lista
            resultado.append(sis)

        return resultado

    @classmethod
    def obter_menus_por_usuario(cls, usuario_rede: str) -> list[dict]:
        if not usuario_rede or not usuario_rede.strip():
            raise ValueError("O código do usuário de rede é obrigatório.")
        linhas = AcessoRepository.buscar_permissoes_usuario(usuario_rede.strip())
        return cls.construir_arvore_menus(linhas)

    @staticmethod
    def obter_os_pendentes(usuario_rede: str) -> list[dict]:
        if not usuario_rede or not usuario_rede.strip():
            raise ValueError("O código do usuário de rede é obrigatório.")
        return AcessoRepository.listar_os_pendentes(usuario_rede.strip())

    @staticmethod
    def dar_ciencia_os(id_ciencia: int, usuario_rede: str) -> bool:
        if not id_ciencia or id_ciencia <= 0:
            raise ValueError("ID da ciência inválido.")
        if not usuario_rede or not usuario_rede.strip():
            raise ValueError("O código do usuário de rede é obrigatório.")
        return AcessoRepository.confirmar_ciencia(id_ciencia, usuario_rede.strip())
