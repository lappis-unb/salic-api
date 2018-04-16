from ..query import Query
from ...models import Agentes, Nomes, Internet, \
    ComprovantePagamento as Comprovante, \
    ComprovantePagamentoxPlanilhaAprovacao as ComprovanteAprovacao, \
    PlanilhaAprovacao, PlanilhaItens, Arquivo, Projeto


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
        'tipo_documento': Comprovante.tpDocumentoLabel,
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
                 .filter(Agentes.CNPJCPF.like(cgccpf)))

        return query
