from datetime import datetime

from salic_api.models import ComprovantePagamentoxPlanilhaAprovacao, \
    ComprovantePagamento, ArquivoImagem, Documento, \
    DocumentoProjeto, ItemCusto


def tbcomprovantepagamentoxplanilhaaprovacao_example(size=1):
    return [ComprovantePagamentoxPlanilhaAprovacao(
        idPlanilhaAprovacao=i,
        idComprovantePagamento=i,
        DtEmissao=datetime(2000, 1, 1),
        vlComprovado=2000.0,)
        for i in range(1, size + 1)
    ]


def tbcomprovantepagamento_example(size=1):
    return [ComprovantePagamento(
        idComprovantePagamento=i,
        idFornecedor=i,
        idArquivo=i,
        tpFormaDePagamento='1',
        nrComprovante='%s' % i,
        nrDocumentoDePagamento='%s' % i,
        vlComprovacao=3.1415,
        tpDocumento=i,
        DtPagamento=datetime(2000, 2, 2),
        dtEmissao=datetime(2000, 1, 1),
        dsJustificativa='Descricao Justificativa',)
        for i in range(1, size + 1)]


def arquivo_imagem_example(size=1):
    return [ArquivoImagem(
        idArquivoImagem=i,
        idArquivo=i,
        imagem="This should be an image",
        dsDocumento="dsDocumento",)
        for i in range(1, size + 1)
    ]


def documento_example(size=1):
    return [Documento(
        idDocumento=i,
        idArquivo=i,)
        for i in range(1, size + 1)
    ]


def documento_projeto_example(size=1):
    return [DocumentoProjeto(
        idDocumentoProjeto=i,
        idDocumento=i,
        idTipoDocumento=i,
        idPronac=20001234,)
        for i in range(1, size + 1)
    ]


def tbItemCusto_example(size=1):
    return [ItemCusto(
        idItem=i,
        dsMarca='Descricao marca',
        dsFabricante='Descricao fabricante',
        dsItemDeCusto='Descricao item',
        idPlanilhaAprovacao=i)
        for i in range(1, size + 1)
    ]
