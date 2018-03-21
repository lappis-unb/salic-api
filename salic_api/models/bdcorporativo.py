from sqlalchemy import Column, Integer, ForeignKey, Float, String, case

from .base import *


class ItemCusto(ItemCustoBase, Base):
    idItem = Column(Integer, primary_key=True)
    idPlanilhaAprovacao = Column(Integer, ForeignKey(
        foreign_key(PlanilhaAprovacaoBase, 'idPlanilhaAprovacao')))
    dsItemDeCusto=Column(String)
    dsMarca=Column(String)
    dsFabricante=Column(String)


class ComprovantePagamentoxPlanilhaAprovacao(ComprovantePagamentoxPlanilhaAprovacaoBase, Base):  # noqa: N801
    idPlanilhaAprovacao=Column(Integer, primary_key=True)
    idComprovantePagamento=Column(
        Integer,
        ForeignKey(foreign_key(ComprovantePagamentoBase, 'idComprovantePagamento')))
    vlComprovado=Column(Float)
    DtEmissao=Column(DateTime)


class ComprovantePagamento(ComprovantePagamentoBase, Base):  # noqa: N801
    idComprovantePagamento=Column(Integer, primary_key=True)
    idFornecedor=Column(Integer)
    idArquivo=Column(Integer, ForeignKey(foreign_key(ArquivoBase, 'idArquivo')))
    DtPagamento=Column(DateTime)
    tpDocumento=Column(Integer)
    dtEmissao=Column(DateTime)
    tpFormaDePagamento=Column(String)
    nrDocumentoDePagamento=Column(String)
    nrComprovante=Column(String)
    dsJustificativa=Column(String)
    vlComprovacao=Column(Float)

    # Computed properties
    tpFormaDePagamentoLabel=case(
        [
            (tpFormaDePagamento == 1, 'Cheque'),
            (tpFormaDePagamento == 2, 'Transferencia Bancaria'),
            (tpFormaDePagamento == 3, 'Saque/Dinheiro'),
        ],
        else_='',
    )

    tpDocumentoLabel=case(
        [
            (tpDocumento == 1, 'Boleto Bancario'),
            (tpDocumento == 2, 'Cupom Fiscal'),
            (tpDocumento == 3, 'Nota Fiscal / Fatura'),
            (tpDocumento == 4, 'Recibo de Pagamento'),
            (tpDocumento == 5, 'RPA'),
        ],
        else_='Nao identificado',
    )


class Arquivo(ArquivoBase, Base):  # noqa: N801
    idArquivo=Column(Integer, primary_key=True)
    nmArquivo=Column(String)


class ArquivoImagem(ArquivoImagemBase, Base):
    idArquivoImagem=Column(Integer, primary_key=True)
    idArquivo=Column(Integer, ForeignKey(foreign_key(ArquivoBase, "idArquivo")))
    imagem=Column(String)
    dsDocumento=Column(String)


class Documento(DocumentoBase, Base):
    idDocumento=Column(Integer, primary_key=True)
    idArquivo=Column(Integer, ForeignKey(foreign_key(ArquivoBase, "idArquivo")))


class DocumentoProjeto(DocumentoProjetoBase, Base):
    idDocumentoProjeto=Column(Integer, primary_key=True)
    idDocumento=Column(Integer, ForeignKey(foreign_key(DocumentoBase, "idDocumento")))
    idTipoDocumento=Column(Integer)
    idPronac=Column(Integer)
