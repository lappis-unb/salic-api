import pytest


@pytest.mark.usefixtures('db_data')
class TestCsv:
    def test_incentivador_csv(self, client):
        url = '/v1/incentivadores/30313233343536373839616263646566e0797636'
        expected = INCENTIVADOR_CSV
        check_csv(client, url, expected)

    def test_proponente_csv(self, client):
        url = '/v1/proponentes/30313233343536373839616263646566e0797636'
        expected = PROPONENTE_CSV
        check_csv(client, url, expected)

    def test_preprojeto_csv(self, client):
        url = '/v1/propostas/1'
        expected = PROPOSTA_CSV
        check_csv(client, url, expected)

    def test_fornecedor_csv(self, client):
        url = '/v1/fornecedores/3343c59a47414d4dd0294c6f36035e00eda6bd74'
        expected = FORNECEDOR_CSV
        check_csv(client, url, expected)

    def test_projeto_csv(self, client):
        url = '/v1/projetos/20001234'
        expected = PROJETO_CSV
        check_csv(client, url, expected)


def check_csv(client, url, expected):
    response = client.get(url + '?format=csv')
    result = response.get_data(as_text=True)
    assert result == expected


INCENTIVADOR_CSV = """cgccpf,nome,responsavel,tipo_pessoa,UF,municipio,total_doado
1234,Nome,Responsavel,juridica,Uf,Cidade,0.0
""".replace('\n', '\r\n')


PROPONENTE_CSV = """cgccpf,nome,responsavel,tipo_pessoa,UF,total_captado,municipio
1234,Nome,Responsavel,juridica,Uf,1000,Cidade
""".replace('\n', '\r\n')

PROPOSTA_CSV = (
    "impacto_ambiental,ficha_tecnica,data_termino,id,mecanismo,"
    "data_arquivamento,data_inicio,democratizacao,data_aceite,sinopse,nome,"
    "estrategia_execucao,especificacao_tecnica,acessibilidade,objetivos,etapa,"
    "resumo,justificativa\r\n"

    "ImpactoAmbiental,FichaTecnica,2000-02-01,1,Mecenato,2000-03-01,2000-01-01,"
    "DemocratizacaoDeAcesso,2000-01-01,Sinopse,Test,EstrategiadeExecucao,"
    "EspecificacaoTecnica,Acessibilidade,cultural,"
    "EtapaDeTrabalho,ResumoDoProjeto,Justificativa\r\n")

FORNECEDOR_CSV = """email,nome,cgccpf
email,Name,1234
""".replace('\n', '\r\n')

PROJETO_CSV = (
    "objetivos,cgccpf,valor_captado,situacao,data_termino,PRONAC,valor_solicitado,"
    "etapa,segmento,acessibilidade,especificacao_tecnica,sinopse,valor_projeto,"
    "enquadramento,UF,justificativa,providencia,proponente,democratizacao,"
    "data_inicio,ficha_tecnica,mecanismo,impacto_ambiental,nome,"
    "estrategia_execucao,resumo,outras_fontes,municipio,valor_aprovado,"
    "valor_proposta,ano_projeto,area,code,message\r\n"

    "cultural,1234,1000,Descricao,2000-02-01,20001234,1000,EtapaDeTrabalho,"
    "Teatro,Acessibilidade,EspecificacaoTecnica,Sinopse,1000,Artigo 26,DF,"
    "Justificativa,nenhuma,Nome,DemocratizacaoDeAcesso,2000-01-01,FichaTecnica,"
    "Mecenato,ImpactoAmbiental,Test,EstrategiadeExecucao,ResumoDoProjeto,0,"
    "Cidade,1000,1000,2000,Artes Cênicas,,\r\n")
