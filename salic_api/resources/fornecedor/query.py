from sqlalchemy.sql import text

from ..query import Query
from ..serialization import listify_queryset
from ...models import Agentes, Nomes, Internet, \
    ComprovantePagamento as Comprovante, \
    ComprovantePagamentoxPlanilhaAprovacao as ComprovanteAprovacao, \
    PlanilhaAprovacao, PlanilhaItens, Arquivo, Produto, Projeto


class FornecedorQuery(Query):
    """
    Responsável por criar a query da tabela Fornecedor
    """

    labels_to_fields = {
        'cgccpf': Agentes.CNPJCPF,
        'nome': Nomes.Descricao,
        'email': Internet.Descricao,
    }

    def query(self, limit=1, offset=0, cgccpf=None, PRONAC=None, nome=None):
        query = self.raw_query(*self.query_fields)
        query = query.select_from(ComprovanteAprovacao).distinct()
        query = (query
                 .join(Comprovante,
                       ComprovanteAprovacao.idComprovantePagamento ==
                       Comprovante.idComprovantePagamento)
                 .outerjoin(Agentes,
                            Comprovante.idFornecedor == Agentes.idAgente)
                 .outerjoin(Nomes,
                            Comprovante.idFornecedor == Nomes.idAgente)
                 .outerjoin(Internet,
                            Comprovante.idFornecedor == Internet.idAgente)
                 .outerjoin(PlanilhaAprovacao,
                            ComprovanteAprovacao.idPlanilhaAprovacao ==
                            PlanilhaAprovacao.idPlanilhaAprovacao)
                 # FIXME: check if the explicit equality test is necessary
                 # now that we have a FK constraint
                 .outerjoin(PlanilhaItens,
                            PlanilhaAprovacao.idPlanilhaItem ==
                            PlanilhaItens.idPlanilhaItens)
                 .outerjoin(Arquivo,
                            Comprovante.idArquivo == Arquivo.idArquivo)

                 )

        query = query.filter(Agentes.CNPJCPF.isnot(None))

        query = query.join(Projeto,
                PlanilhaAprovacao.idPronac == Projeto.IdPRONAC)

        if PRONAC is not None:
            query = query.filter((Projeto.AnoProjeto + Projeto.Sequencial)
                                 .like(PRONAC))

        return query

    def count(self, cgccpf=None, PRONAC=None, nome=None):
        if cgccpf is not None:
            query = text(FORNECEDOR_COUNT_CGCCPF)
            result = self.sql_connector.session.execute(
                query, {'cgccpf': '%{}%'.format(cgccpf)}).fetchall()

        elif nome is not None:
            query = text(FORNECEDOR_COUNT_NOME)
            result = self.sql_connector.session.execute(
                query, {'nome': '%{}%'.format(nome)}).fetchall()

        elif PRONAC is not None:
            query = text(FORNECEDOR_COUNT_PRONAC)
            result = self.sql_connector.session.execute(
                query, {'PRONAC': PRONAC}).fetchall()

        else:
            query = text(FORNECEDOR_COUNT)
            result = self.session.execute(query, {}).fetchall()

        n_records = listify_queryset(result)
        return n_records[0]['total']


class ProductQuery(Query):
    """

    """
    labels_to_fields = {
        'nome': PlanilhaItens.Descricao,
        'id_comprovante_pagamento': Comprovante.idComprovantePagamento,
        'id_planilha_aprovacao': ComprovanteAprovacao.idPlanilhaAprovacao,
        'cgccpf': Agentes.CNPJCPF,
        'nome_fornecedor': Nomes.Descricao,
        'data_aprovacao': Comprovante.DtPagamento,
        'PRONAC': Projeto.AnoProjeto + Projeto.Sequencial,
        'tipo_documento': Comprovante.tpDocumento,
        'nr_comprovante': Comprovante.nrComprovante,
        'data_pagamento': Comprovante.dtEmissao,
        'tipo_forma_pagamento': Comprovante.tpFormaDePagamentoLabel,
        'nr_documento_pagamento': Comprovante.nrDocumentoDePagamento,
        'valor_pagamento': ComprovanteAprovacao.vlComprovado,
        'id_arquivo': Comprovante.idArquivo,
        'justificativa': Comprovante.dsJustificativa,
        'nm_arquivo': Arquivo.nmArquivo,
    }

    def query(self, cgccpf, limit=100, offset=0):
        query = self.raw_query(*self.query_fields)

        query = query.select_from(ComprovanteAprovacao)
        query = (query
                 .join(Comprovante,
                       ComprovanteAprovacao.idComprovantePagamento ==
                       Comprovante.idComprovantePagamento)
                 .outerjoin(PlanilhaAprovacao,
                            ComprovanteAprovacao.idPlanilhaAprovacao == PlanilhaAprovacao.idPlanilhaAprovacao)
                 .outerjoin(PlanilhaItens,
                            PlanilhaAprovacao.idPlanilhaItem == PlanilhaItens.idPlanilhaItens)
                 .outerjoin(Nomes,
                            Comprovante.idFornecedor == Nomes.idAgente)
                 .outerjoin(Arquivo,
                            Comprovante.idArquivo == Arquivo.idArquivo)
                 .outerjoin(Projeto,
                            PlanilhaAprovacao.idPronac == Projeto.IdPRONAC)
                 .outerjoin(Agentes,
                            Comprovante.idFornecedor == Agentes.idAgente)
                 .filter(Agentes.CNPJCPF.like(cgccpf))
                )

        return query


FORNECEDOR_CGCCPF = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (g.CNPJCPF LIKE :cgccpf) AND g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR_NOME = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (e.Descricao LIKE :nome) AND g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR_PRONAC = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE (Projetos.AnoProjeto + Projetos.Sequencial = :PRONAC) AND g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR = """
SELECT
   DISTINCT g.CNPJCPF as cgccpf, e.Descricao as nome, Internet.Descricao as email

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE g.CNPJCPF IS NOT NULL

   ORDER BY cgccpf
   OFFSET :offset ROWS
   FETCH NEXT :limit ROWS ONLY;
"""

FORNECEDOR_COUNT_CGCCPF = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (g.CNPJCPF LIKE :cgccpf) AND g.CNPJCPF IS NOT NULL
"""

FORNECEDOR_COUNT_NOME = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente

   WHERE (e.Descricao LIKE :nome) AND g.CNPJCPF IS NOT NULL
"""

FORNECEDOR_COUNT_PRONAC = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE (Projetos.AnoProjeto + Projetos.Sequencial = :PRONAC) AND g.CNPJCPF IS NOT NULL
"""

FORNECEDOR_COUNT = """
SELECT
   COUNT(DISTINCT g.CNPJCPF) AS total

   FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
   INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
   LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS PlanilhaAprovacao ON a.idPlanilhaAprovacao = PlanilhaAprovacao.idPlanilhaAprovacao
   LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON PlanilhaAprovacao.idPlanilhaItem = d.idPlanilhaItens
   LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
   LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
   LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente
   LEFT JOIN Agentes.dbo.Internet AS Internet ON b.idFornecedor = Internet.idAgente
   JOIN SAC.dbo.Projetos AS Projetos ON PlanilhaAprovacao.idPronac = Projetos.IdPRONAC

   WHERE g.CNPJCPF IS NOT NULL
"""
