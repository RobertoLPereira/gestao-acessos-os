from database import get_connection

class AcessoRepository:
    @staticmethod
    def buscar_permissoes_usuario(usuario_rede: str) -> list[dict]:
        sql = """
            SELECT 
                idsistema, nomesistema, sigla_sistema, url_sistema,
                idmodulomenu, menu, urlmenu,
                idtransacoes, transacao, urltransacao,
                idsubtransacao, subtransacao
            FROM seguranca."PermissoesWs"
            WHERE LOWER(codigousuariorede) = LOWER(%s)
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (usuario_rede,))
                return cur.fetchall()

    @staticmethod
    def listar_os_pendentes(usuario_rede: str) -> list[dict]:
        sql = """
            SELECT 
                os.idordemservico,
                os.datacadastro,
                os.datainiciovalidade,
                os.datafimvalidade,
                os.corpo,
                osc.idordemservicociencia,
                osc.status
            FROM seguranca.ordemservicocorpo os
            JOIN seguranca.ordemservicociencia osc ON os.idordemservico = osc.idordemservico
            WHERE LOWER(osc.codigousuariorede) = LOWER(%s)
              AND osc.status <> 0
              AND CURRENT_DATE BETWEEN os.datainiciovalidade AND os.datafimvalidade
            ORDER BY os.idordemservico DESC
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (usuario_rede,))
                return cur.fetchall()

    @staticmethod
    def confirmar_ciencia(id_ciencia: int, usuario_rede: str) -> bool:
        sql = """
            UPDATE seguranca.ordemservicociencia
            SET status = 0, dataciencia = CURRENT_DATE
            WHERE idordemservicociencia = %s
              AND LOWER(codigousuariorede) = LOWER(%s)
              AND status <> 0
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (id_ciencia, usuario_rede))
                atualizado = cur.rowcount > 0
            conn.commit()
        return atualizado
