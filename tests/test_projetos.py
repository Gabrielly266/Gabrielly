import importlib.util
import tempfile
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]


def carregar_modulo(nome, caminho):
    especificacao = importlib.util.spec_from_file_location(nome, RAIZ / caminho)
    modulo = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(modulo)
    return modulo


sgc = carregar_modulo("sgc", "projetos/gestao-conhecimento-sgc/sgc.py")
painel = carregar_modulo(
    "painel_governanca", "projetos/painel-governanca-ti/painel_governanca.py"
)
cobit = carregar_modulo(
    "governanca_cobit", "projetos/governanca-cobit/governanca_cobit.py"
)
transacoes = carregar_modulo(
    "processamento_transacoes",
    "projetos/processamento-transacoes/processamento_transacoes.py",
)
auditoria = carregar_modulo("auditoria", "projetos/auditoria-acessos/auditoria.py")


class ProjetosTestCase(unittest.TestCase):
    def test_pesquisa_encontra_artigo_por_conteudo(self):
        base = sgc.carregar_dados(Path("/tmp/base_inexistente_gabrielly.json"))
        resultado = sgc.buscar_conhecimento(base, "sql")
        self.assertEqual(resultado[0]["titulo"], "Consultas em banco de dados")

    def test_base_de_conhecimento_persiste_em_json(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "base.json"
            base = []
            artigo = sgc.adicionar_conhecimento(base, "Título", "Conteúdo")
            sgc.salvar_dados(base, arquivo)
            self.assertEqual(sgc.carregar_dados(arquivo), [artigo])

    def test_painel_consolida_incidentes(self):
        incidentes, problemas = painel.criar_bases_de_exemplo()
        resultado = painel.montar_painel(incidentes, problemas)
        self.assertEqual(int(resultado.loc["Serviço A", "total_incidentes"]), 2)
        self.assertEqual(painel.resumir_painel(resultado)["percentual_com_problema"], 66.7)

    def test_cobit_classifica_dominios(self):
        self.assertEqual(cobit.classificar_dominio_cobit("Projeto de exemplo"), "BAI")
        self.assertEqual(cobit.classificar_dominio_cobit("Conformidade"), "MEA")

    def test_cobit_calcula_maturidade(self):
        notas = {dominio: 3.0 for dominio in cobit.PALAVRAS_POR_DOMINIO}
        self.assertAlmostEqual(cobit.calcular_maturidade_customizada(notas), 3.0)

    def test_transacao_recebe_desconto(self):
        evento = {"cliente": "Cliente_1", "valor": 1200.0, "vip": False}
        resultado = transacoes.processar_transacao(evento)
        self.assertEqual(resultado["valor"], 1020.0)
        self.assertTrue(resultado["desconto_aplicado"])
        self.assertEqual(evento["valor"], 1200.0)

    def test_clientes_vip_nao_geram_alertas(self):
        eventos = [{"cliente": "Cliente_1", "valor": 100.0, "vip": True}] * 3
        self.assertEqual(transacoes.identificar_alertas(eventos), {})

    def test_auditoria_identifica_riscos_dos_dados_de_exemplo(self):
        logs, usuarios = auditoria.carregar_bases()
        resultado = auditoria.auditar_acessos(logs, usuarios)
        self.assertEqual(resultado["total"], 4)
        self.assertEqual(len(resultado["contas_orfas"]), 1)
        self.assertEqual(len(resultado["fora_horario"]), 1)
        self.assertEqual(len(resultado["ips_externos"]), 1)


if __name__ == "__main__":
    unittest.main()
