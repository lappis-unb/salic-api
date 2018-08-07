import graphene

from sqlalchemy import func
from graphene.types.scalars import Scalar

from ..resources.incentivador.query import IncentivadorQuery
from ..resources.incentivador.incentivador_list import IncentivadorList

from ..resources.estatistica.contagem import (
    IncentivadorUFQuery, ProponenteUFQuery,
    IncentivadorRegiaoQuery, ProponenteRegiaoQuery,
    ProjetoUFQuery, ProjetoRegiaoQuery, SegmentoCountQuery,
    AreaCountQuery, result_to_dict)

from ..resources.incentivador.query import DoacaoQuery
from ..resources.incentivador.doacao import DoacaoList

from ..resources.preprojeto.query import PreProjetoQuery
from ..resources.preprojeto.pre_projeto_list import PreProjetoList

from ..resources.projeto.projeto_list import ProjetoList
from ..resources.projeto.query import (
    ProjetoQuery, CertidoesNegativasQuery, DivulgacaoQuery, DeslocamentoQuery,
    DistribuicaoQuery, ReadequacaoQuery, CaptacaoQuery, AreasSegmentosQuery)

from ..resources.proponente.query import ProponenteQuery
from ..resources.proponente.proponente_list import ProponenteList

from ..resources.fornecedor.query import FornecedorQuery, ProductQuery
from ..resources.fornecedor.fornecedor_list import FornecedorList

from ..resources.fornecedor.produto import Produto

from ..query_helpers import resolve



class ObjectField(Scalar):

    @staticmethod
    def serialize(dt):
        return dt

    @staticmethod
    def parse_literal(node):
        return node.value

    @staticmethod
    def parse_value(value):
        return value


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
            'limit': graphene.Int(description='Limite da quantidade de resultados'),
            'offset': graphene.Int(description='Deslocamento dos resultados da busca. offset:10 pula os 10 primeiros resultados'),
            'order': graphene.String(description='Se a ordenacao será crescente(padrão) ou decrescente. Ex.: order:"desc"'),
            'sort': graphene.String(description='Como ordenar o resultado. Ex.: sort:"campo" ordenaria resultados pelo campo'),
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

    def resolve_incentivadores_por_uf(self, info, **kwargs):
        query_result = resolve(IncentivadorUFQuery, IncentivadorUFQuery, kwargs)
        return result_to_dict(query_result)

    def resolve_proponentes_por_uf(self, info, **kwargs):
        query_result = resolve(ProponenteUFQuery, ProponenteUFQuery, kwargs)
        return result_to_dict(query_result)

    def resolve_proponentes_por_regiao(self, info, **kwargs):
        query_result = resolve(ProponenteRegiaoQuery, ProponenteRegiaoQuery, kwargs)
        return result_to_dict(query_result)

    def resolve_incentivadores_por_regiao(self, info, **kwargs):
        query_result = resolve(IncentivadorRegiaoQuery, IncentivadorRegiaoQuery, kwargs)
        return result_to_dict(query_result)

    def resolve_projetos_por_uf(self, info, **kwargs):
        query_result = resolve(ProjetoUFQuery, ProjetoUFQuery, kwargs)
        return result_to_dict(query_result)

    def resolve_projetos_por_regiao(self, info, **kwargs):
        query_result = resolve(ProjetoRegiaoQuery, ProjetoRegiaoQuery, kwargs)
        return result_to_dict(query_result)

    def resolve_total_por_segmento(self, info, **kwargs):
        query_result = resolve(SegmentoCountQuery, SegmentoCountQuery, kwargs).all()
        return result_to_dict(query_result)

    def resolve_total_por_area(self, info, **kwargs):
        query_result = resolve(AreaCountQuery, AreaCountQuery, kwargs).all()
        return result_to_dict(query_result)

    def resolve_areas(self, info, **kwargs):
        query_result = AreasSegmentosQuery().query().all()
        result={}
        for obj in query_result:
            if obj.area in result.keys():
                result[obj.area] += [obj.segment]
            else:
                result[obj.area] = [obj.segment]
        return result

class DoacaoType(CommonFields, graphene.ObjectType):
    # Pronac do projeto associado a doacao
    PRONAC = graphene.String(description='Pronac do projeto associado')
    valor = graphene.String(description='Valor doado')
    data_recibo = graphene.String(description='data do recibo')
    nome_projeto = graphene.String(description='Nome do projeto para onde a doação foi feita')
    cgccpf = graphene.String(description='CPF ou CNPJ do doador')
    nome_doador = graphene.String(description='Nome do doador')


class IncentivadorType(CommonFields, graphene.ObjectType, Resolvers):
    nome = graphene.String(description='Nome do incentivador')
    municipio = graphene.String(description='Município')
    UF = graphene.String(description='Unidade Federativa')
    responsavel = graphene.String(description='Responsável')
    cgccpf = graphene.String(description='CPF ou CPNJ do incentivador')
    total_doado = graphene.Float(description='Soma de todas as doações feitas pelo incentivador')
    tipo_pessoa = graphene.String(description='Informa se o incentivador é pessoa física ou jurídica')

    doacoes = graphene.List(DoacaoType, **DoacaoType.fields(), description='Doações feitas por esse incentivador')


class ProponenteType(CommonFields, graphene.ObjectType, Resolvers):
    total_captado = graphene.Float()
    nome = graphene.String()
    municipio = graphene.String()
    UF = graphene.String(description="Unidade Federativa")
    responsavel = graphene.String()
    cgccpf = graphene.String(description='CPF ou CNPJ do proponente')
    tipo_pessoa = graphene.String(description='Informa se o incentivador é pessoa física ou jurídica')


class ProdutoType(CommonFields, graphene.ObjectType, Resolvers):
    nome = graphene.String()
    id_comprovante_pagamento = graphene.Int()
    id_planilha_aprovacao = graphene.Int()
    cgccpf = graphene.String()
    nome_fornecedor = graphene.String()
    data_aprovacao = graphene.String(description='Data em formato aaaa-mm-dd')
    PRONAC = graphene.String(description='Pronac do projeto associado')
    tipo_documento = graphene.String()
    nr_comprovante = graphene.String()
    data_pagamento = graphene.String(description='Data em formato aaaa-mm-dd')
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

    produtos_count = graphene.Int()
    def resolve_produtos_count(self, info, **kwargs):
        return resolve(ProductQuery, Produto, kwargs).count()

class CertidoesNegativasType(graphene.ObjectType, Resolvers):
    data_emissao = graphene.String(description='Data em formato aaaa-mm-dd')
    data_validade = graphene.String(description='Data em formato aaaa-mm-dd')
    descricao = graphene.String()
    situacao = graphene.String()


class DivulgacaoType(graphene.ObjectType, Resolvers):
    peca = graphene.String()
    veiculo = graphene.String()


class DeslocamentoType(CommonFields, graphene.ObjectType):
    id_deslocamento = graphene.Int()
    id_projeto = graphene.Int()
    PaisOrigem = graphene.String()
    PaisDestino = graphene.String()
    UFOrigem = graphene.String(description="Unidade Federativa de origem")
    UFDestino = graphene.String(description="Unidade Federativa de destino")
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
    data_solicitacao = graphene.String(description='Data em formato aaaa-mm-dd')
    descricao_solicitacao = graphene.Int()
    descricao_justificativa = graphene.String()
    id_solicitante = graphene.Int()
    id_avaliador = graphene.Int()
    data_avaliador = graphene.String(description='Data em formato aaaa-mm-dd')
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
    data_pedido = graphene.String(description='Data em formato aaaa-mm-dd')
    data_inicio = graphene.String(description='Data em formato aaaa-mm-dd')
    data_final = graphene.String(description='Data em formato aaaa-mm-dd')
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
    data_aprovacao = graphene.String(description='Data em formato aaaa-mm-dd')
    tipo_documento = graphene.String()
    nr_comprovante = graphene.String()
    data_pagamento = graphene.String(description='Data em formato aaaa-mm-dd')
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
    data_recibo = graphene.String(description='Data em formato aaaa-mm-dd')
    cgccpf = graphene.String()
    nome_projeto = graphene.String()
    nome_doador = graphene.String()


class ProjetoType(CommonFields, graphene.ObjectType, Resolvers):
    nome = graphene.String()
    providencia = graphene.String()
    PRONAC = graphene.String(description='Pronac do projeto associado')
    IdPRONAC = graphene.String()
    UF = graphene.String(description="Unidade Federativa")
    data_inicio = graphene.String(description='Data em formato aaaa-mm-dd')
    data_termino = graphene.String(description='Data em formato aaaa-mm-dd')
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

    query_warning = (
    "*CUIDADO* - "
    "Utilize apenas para um único projeto(com filtro de pronac) ou "
    "quantidade mínima de projetos.")
    #  Detail info
    certidoes_negativas = graphene.List(CertidoesNegativasType,
                                        description=query_warning)
    divulgacoes = graphene.List(DivulgacaoType,
                                        description=query_warning)
    deslocamentos = graphene.List(DeslocamentoType,
                                        description=query_warning)
    distribuicoes = graphene.List(DistribuicaoType,
                                        description=query_warning)
    readequacoes = graphene.List(ReadequacaoType,
                                        description=query_warning)
    prorrogacoes = graphene.List(ProrrogacaoType,
                                        description=query_warning)

    relacoes_pagamentos = graphene.List(RelacaoPagamentoType,
                                        description=query_warning)
    relatorios_fiscos = graphene.List(RelatorioFiscoType,
                                        description=query_warning)
    bens_de_capital = graphene.List(BensDeCapitalType,
                                        description=query_warning)
    captacoes = graphene.List(CaptacaoType,
                                        description=query_warning)


class PropostaType(CommonFields, graphene.ObjectType, Resolvers):
    id = graphene.Int(description='id da proposta')
    nome = graphene.String(description='Nome do Projeto')
    data_inicio = graphene.String(description='Data em formato aaaa-mm-dd')
    data_termino = graphene.String(description='Data em formato aaaa-mm-dd')
    data_aceite = graphene.String(description='Data em formato aaaa-mm-dd')
    data_arquivamento = graphene.String(description='Data em formato aaaa-mm-dd')
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

    # projeto join fields
    UF = graphene.String()
    PRONAC = graphene.String()
    situacao = graphene.String()

    # Area join fields
    area = graphene.String() # Area.Descricao


class DoacaoGQLQuery(graphene.ObjectType, Resolvers):
    doacoes = graphene.List(DoacaoType, **DoacaoType.fields(),
                            description='Doações feitas para projetos')


class DeslocamentosGQLQuery(graphene.ObjectType, Resolvers):
    deslocamentos = graphene.List(DeslocamentoType, **DeslocamentoType.fields())


class IncentivadorGQLQuery(graphene.ObjectType, Resolvers):
    description='Pessoa(física/jurídica) que realizou alguma doação'
    incentivadores = graphene.List(IncentivadorType,
                                   **IncentivadorType.fields(),
                                   description=description)


class PropostaGQLQuery(graphene.ObjectType, Resolvers):
    description='Propostas de projeto'
    propostas = graphene.List(PropostaType, **PropostaType.fields(),
                              description=description)


class ProponenteGQLQuery(graphene.ObjectType, Resolvers):
    description='Criador de proposta(s)'
    proponentes = graphene.List(ProponenteType, **ProponenteType.fields(),
                                description=description)


class FornecedorGQLQuery(graphene.ObjectType, Resolvers):
    description=("Pessoa(física/jurídica) que"
        " fornece produto ou serviço para um projeto")
    fornecedores = graphene.List(FornecedorType, **FornecedorType.fields(),
                                 description=description)


class ProjetoGQLQuery(graphene.ObjectType, Resolvers):
    description='Projetos culturais'
    projetos = graphene.List(ProjetoType, **ProjetoType.fields(),
                             description=description)


class AreaGQLQuery(graphene.ObjectType, Resolvers):
    areas = ObjectField()

class UFCountGQLQuery(graphene.ObjectType, Resolvers):
    filters =  {
        'segmento': graphene.String(),
        'area': graphene.String(),
        'situacao': graphene.String(),
        'mecanismo': graphene.String(),
        'enquadramento': graphene.String(),
        'UF': graphene.String(),
        'ano_projeto': graphene.String(),
        'nome': graphene.String()
    }

    proponentes_por_uf = ObjectField(**filters)
    proponentes_por_regiao = ObjectField(**filters)
    incentivadores_por_uf = ObjectField(**filters)
    incentivadores_por_regiao = ObjectField(**filters)
    projetos_por_uf = ObjectField(**filters)
    projetos_por_regiao = ObjectField(**filters)

    total_por_segmento = ObjectField({'limit': graphene.Int(), 'ano_projeto': graphene.String()})
    total_por_area = ObjectField({'limit': graphene.Int(), 'ano_projeto': graphene.String()})
