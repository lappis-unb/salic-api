import graphene

from ..resources.incentivador.query import IncentivadorQuery
from ..resources.incentivador.incentivador_list import IncentivadorList

from ..resources.incentivador.query import DoacaoQuery
from ..resources.incentivador.doacao import DoacaoList

from ..resources.preprojeto.query import PreProjetoQuery
from ..resources.preprojeto.pre_projeto_list import PreProjetoList

from ..resources.projeto.projeto_list import ProjetoList
from ..resources.projeto.query import (
    ProjetoQuery, CertidoesNegativasQuery, DivulgacaoQuery, DeslocamentoQuery,
    DistribuicaoQuery, ReadequacaoQuery, CaptacaoQuery)

from ..resources.proponente.query import ProponenteQuery
from ..resources.proponente.proponente_list import ProponenteList

from ..resources.fornecedor.query import FornecedorQuery, ProductQuery
from ..resources.fornecedor.fornecedor_list import FornecedorList

from ..resources.fornecedor.produto import Produto

from ..query_helpers import resolve


def inject_arg(argument):
    """
    Injects the given argument from the type to the query
    """

    def real_decorator(target):
        def wrapper(*args, **kwargs):
            data_to_inject = getattr(args[0], argument, None)
            kwargs[argument] = data_to_inject
            return target(*args, **kwargs)

        return wrapper

    return real_decorator


class CommonFields:
    @classmethod
    def fields(cls):
        class_fields = {
            k: getattr(cls, k)
            for k in dir(cls) if isinstance(getattr(cls, k), graphene.Scalar)
        }
        return {
            'limit': graphene.Int(),
            'offset': graphene.Int(),
            'order': graphene.String(),
            'sort': graphene.String(),
            **class_fields
        }


class Resolvers:
    @inject_arg('cgccpf')
    def resolve_doacoes(self, info, **kwargs):
        return resolve(DoacaoQuery, DoacaoList, kwargs)

    def resolve_incentivadores(self, info, **kwargs):
        return resolve(IncentivadorQuery, IncentivadorList, kwargs)

    def resolve_propostas(self, info, **kwargs):
        return resolve(PreProjetoQuery, PreProjetoList, kwargs)

    def resolve_proponentes(self, info, **kwargs):
        return resolve(ProponenteQuery, ProponenteList, kwargs)

    def resolve_fornecedores(self, info, **kwargs):
        return resolve(FornecedorQuery, FornecedorList, kwargs)

    @inject_arg('cgccpf')
    def resolve_produtos(self, info, **kwargs):
        return resolve(ProductQuery, Produto, kwargs)

    def resolve_projetos(self, info, **kwargs):
        return resolve(ProjetoQuery, ProjetoList, kwargs)

    @inject_arg('PRONAC')
    def resolve_certidoes_negativas(self, info, **kwargs):
        return CertidoesNegativasQuery().query(**kwargs)

    @inject_arg('PRONAC')
    def resolve_divulgacoes(self, info, **kwargs):
        return DivulgacaoQuery().query(kwargs['PRONAC'])

    @inject_arg('PRONAC')
    def resolve_deslocamentos(self, info, **kwargs):
        return DeslocamentoQuery().query(kwargs['PRONAC'])

    @inject_arg('PRONAC')
    def resolve_distribuicoes(self, info, **kwargs):
        return DistribuicaoQuery().query(kwargs['PRONAC'])

    @inject_arg('IdPRONAC')
    def resolve_readequacoes(self, info, **kwargs):
        return ReadequacaoQuery().query(kwargs['IdPRONAC'])

    @inject_arg('IdPRONAC')
    def resolve_prorrogacoes(self, info, **kwargs):
        return ProjetoQuery().postpone_request(kwargs['IdPRONAC'])

    @inject_arg('IdPRONAC')
    def resolve_relacoes_pagamentos(self, info, **kwargs):
        return ProjetoQuery().payments_listing(idPronac=kwargs['IdPRONAC'])

    @inject_arg('IdPRONAC')
    def resolve_relatorios_fiscos(self, info, **kwargs):
        return ProjetoQuery().taxing_report(kwargs['IdPRONAC'])

    @inject_arg('IdPRONAC')
    def resolve_bens_de_capital(self, info, **kwargs):
        return ProjetoQuery().goods_capital_listing(kwargs['IdPRONAC'])

    @inject_arg('PRONAC')
    def resolve_captacoes(self, info, **kwargs):
        return CaptacaoQuery().query(kwargs['PRONAC'])


class DoacaoType(CommonFields, graphene.ObjectType):
    PRONAC = graphene.String()
    valor = graphene.String()
    data_recibo = graphene.String()
    nome_projeto = graphene.String()
    cgccpf = graphene.String()
    nome_doador = graphene.String()


class IncentivadorType(CommonFields, graphene.ObjectType, Resolvers):
    nome = graphene.String()
    municipio = graphene.String()
    UF = graphene.String()
    responsavel = graphene.String()
    cgccpf = graphene.String()
    total_doado = graphene.Float()
    tipo_pessoa = graphene.String()

    doacoes = graphene.List(DoacaoType, **DoacaoType.fields())


class PropostaType(CommonFields, graphene.ObjectType, Resolvers):
    id = graphene.Int()
    nome = graphene.String()
    data_inicio = graphene.String()
    data_termino = graphene.String()
    data_aceite = graphene.String()
    data_arquivamento = graphene.String()
    acessibilidade = graphene.String()
    objetivos = graphene.String()
    justificativa = graphene.String()
    democratizacao = graphene.String()
    etapa = graphene.String()
    ficha_tecnica = graphene.String()
    resumo = graphene.String()
    sinopse = graphene.String()
    impacto_ambiental = graphene.String()
    especificacao_tecnica = graphene.String()
    estrategia_execucao = graphene.String()
    mecanismo = graphene.String()


class ProponenteType(CommonFields, graphene.ObjectType, Resolvers):
    total_captado = graphene.Int()
    nome = graphene.String()
    municipio = graphene.String()
    UF = graphene.String()
    responsavel = graphene.String()
    cgccpf = graphene.String()
    tipo_pessoa = graphene.String()


class ProdutoType(CommonFields, graphene.ObjectType, Resolvers):
    nome = graphene.String()
    id_comprovante_pagamento = graphene.Int()
    id_planilha_aprovacao = graphene.Int()
    cgccpf = graphene.String()
    nome_fornecedor = graphene.String()
    data_aprovacao = graphene.String()
    PRONAC = graphene.String()
    tipo_documento = graphene.String()
    nr_comprovante = graphene.String()
    data_pagamento = graphene.String()
    tipo_forma_pagamento = graphene.String()
    nr_documento_pagamento = graphene.String()
    valor_pagamento = graphene.Float()
    id_arquivo = graphene.Int()
    justificativa = graphene.String()
    nm_arquivo = graphene.String()


class FornecedorType(CommonFields, graphene.ObjectType, Resolvers):
    cgccpf = graphene.String()
    nome = graphene.String()
    email = graphene.String()

    produtos = graphene.List(ProdutoType, **ProdutoType.fields())


class CertidoesNegativasType(graphene.ObjectType, Resolvers):
    data_emissao = graphene.String()
    data_validade = graphene.String()
    descricao = graphene.String()
    situacao = graphene.String()


class DivulgacaoType(graphene.ObjectType, Resolvers):
    peca = graphene.String()
    veiculo = graphene.String()


class DeslocamentoType(graphene.ObjectType, Resolvers):
    id_deslocamento = graphene.Int()
    id_projeto = graphene.Int()
    PaisOrigem = graphene.String()
    PaisDestino = graphene.String()
    UFOrigem = graphene.String()
    UFDestino = graphene.String()
    MunicipioOrigem = graphene.String()
    MunicipioDestino = graphene.String()
    Qtde = graphene.Int()


class DistribuicaoType(graphene.ObjectType, Resolvers):
    idPlanoDistribuicao = graphene.Int()
    QtdeVendaNormal = graphene.Int()
    QtdeVendaPromocional = graphene.Int()
    PrecoUnitarioNormal = graphene.Int()
    PrecoUnitarioPromocional = graphene.Int()
    QtdeOutros = graphene.Int()
    QtdeProponente = graphene.Int()
    QtdeProduzida = graphene.Int()
    QtdePatrocinador = graphene.Int()
    area = graphene.String()
    segmento = graphene.String()
    produto = graphene.String()
    posicao_logo = graphene.String()
    Localizacao = graphene.String()


class ReadequacaoType(graphene.ObjectType, Resolvers):
    id_readequacao = graphene.Int()
    data_solicitacao = graphene.String()
    descricao_solicitacao = graphene.Int()
    descricao_justificativa = graphene.String()
    id_solicitante = graphene.Int()
    id_avaliador = graphene.Int()
    data_avaliador = graphene.String()
    descricao_avaliacao = graphene.String()
    id_tipo_readequacao = graphene.Int()
    descricao_readequacao = graphene.String()
    st_atendimento = graphene.String()
    si_encaminhamento = graphene.Int()
    descricao_encaminhamento = graphene.String()
    st_estado = graphene.Boolean()
    id_arquivo = graphene.String()
    nome_arquivo = graphene.String()


class ProrrogacaoType(graphene.ObjectType, Resolvers):
    data_pedido = graphene.String()
    data_inicio = graphene.String()
    data_final = graphene.String()
    observacao = graphene.String()
    atendimento = graphene.String()
    usuario = graphene.String()
    estado = graphene.String()


class RelacaoPagamentoType(graphene.ObjectType, Resolvers):
    nome = graphene.String()
    id_comprovante_pagamento = graphene.Int()
    id_planilha_aprovacao = graphene.Int()
    cgccpf = graphene.String()
    nome_fornecedor = graphene.String()
    data_aprovacao = graphene.String()
    tipo_documento = graphene.String()
    nr_comprovante = graphene.String()
    data_pagamento = graphene.String()
    tipo_forma_pagamento = graphene.String()
    nr_documento_pagamento = graphene.String()
    valor_pagamento = graphene.Float()
    id_arquivo = graphene.Int()
    justificativa = graphene.String()
    nm_arquivo = graphene.String()


class RelatorioFiscoType(graphene.ObjectType, Resolvers):
    id_planilha_etapa = graphene.Int()
    etapa = graphene.String()
    item = graphene.String()
    unidade = graphene.String()
    qtd_programada = graphene.Int()
    valor_programado = graphene.Float()
    perc_executado = graphene.Int()
    perc_a_executar = graphene.Int()
    valor_executado = graphene.Float()


class BensDeCapitalType(graphene.ObjectType, Resolvers):
    Titulo = graphene.String()
    numero_comprovante = graphene.Int()
    Item = graphene.String()
    dtPagamento = graphene.String()
    Especificacao = graphene.String()
    Marca = graphene.String()
    Fabricante = graphene.String()
    Qtde = graphene.Int()
    valor_unitario = graphene.Float()
    valor_total = graphene.Float()


class CaptacaoType(graphene.ObjectType, Resolvers):
    valor = graphene.Float()
    data_recibo = graphene.String()
    cgccpf = graphene.String()
    nome_projeto = graphene.String()
    nome_doador = graphene.String()


class ProjetoType(CommonFields, graphene.ObjectType, Resolvers):
    nome = graphene.String()
    providencia = graphene.String()
    PRONAC = graphene.String()
    IdPRONAC = graphene.String()
    UF = graphene.String()
    data_inicio = graphene.String()
    data_termino = graphene.String()
    ano_projeto = graphene.String()
    acessibilidade = graphene.String()
    objetivos = graphene.String()
    justificativa = graphene.String()
    democratizacao = graphene.String()
    etapa = graphene.String()
    ficha_tecnica = graphene.String()
    resumo = graphene.String()
    sinopse = graphene.String()
    impacto_ambiental = graphene.String()
    especificacao_tecnica = graphene.String()
    estrategia_execucao = graphene.String()
    municipio = graphene.String()
    proponente = graphene.String()
    cgccpf = graphene.String()
    area = graphene.String()
    segmento = graphene.String()
    situacao = graphene.String()
    mecanismo = graphene.String()
    enquadramento = graphene.String()
    valor_solicitado = graphene.Float()
    outras_fontes = graphene.Float()
    valor_captado = graphene.Float()
    valor_proposta = graphene.Float()
    valor_aprovado = graphene.Float()
    valor_projeto = graphene.Float()

    #  Detail info
    certidoes_negativas = graphene.List(CertidoesNegativasType)
    divulgacoes = graphene.List(DivulgacaoType)
    deslocamentos = graphene.List(DeslocamentoType)
    distribuicoes = graphene.List(DistribuicaoType)
    readequacoes = graphene.List(ReadequacaoType)
    prorrogacoes = graphene.List(ProrrogacaoType)

    relacoes_pagamentos = graphene.List(RelacaoPagamentoType)
    relatorios_fiscos = graphene.List(RelatorioFiscoType)
    bens_de_capital = graphene.List(BensDeCapitalType)
    captacoes = graphene.List(CaptacaoType)


class DoacaoGQLQuery(graphene.ObjectType, Resolvers):
    doacoes = graphene.List(DoacaoType, **DoacaoType.fields())


class IncentivadorGQLQuery(graphene.ObjectType, Resolvers):
    incentivadores = graphene.List(IncentivadorType,
                                   **IncentivadorType.fields())


class PropostaGQLQuery(graphene.ObjectType, Resolvers):
    propostas = graphene.List(PropostaType, **PropostaType.fields())


class ProponenteGQLQuery(graphene.ObjectType, Resolvers):
    proponentes = graphene.List(ProponenteType, **ProponenteType.fields())


class FornecedorGQLQuery(graphene.ObjectType, Resolvers):
    fornecedores = graphene.List(FornecedorType, **FornecedorType.fields())


class ProjetoGQLQuery(graphene.ObjectType, Resolvers):
    projetos = graphene.List(ProjetoType, **ProjetoType.fields())
