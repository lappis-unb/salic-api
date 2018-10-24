import operator

from os import environ as env
from sqlalchemy import case, func, and_, or_, cast, Text
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import alias
from sqlalchemy.sql.functions import coalesce

from salic_api.models import PlanoDivulgacao
from ..query import Query, filter_query
from ..resource import InvalidResult
from ...models import (
    ComprovantePagamento as Comprovante, PlanilhaItens, PlanilhaAprovacao,
    ComprovantePagamentoxPlanilhaAprovacao as ComprovanteAprovacao, ItemCusto,
    PlanilhaEtapa, PlanilhaUnidade,
    Projeto, Interessado, Situacao, Enquadramento, PreProjeto,
    Captacao, CertidoesNegativas, Verificacao, PlanoDistribuicao, Produto, Area,
    Segmento, Custos, Mecanismo, Arquivo, ArquivoImagem, Documento,
    DocumentoProjeto, Prorrogacao, Usuarios, Readequacao, TipoReadequacao,
    TipoEncaminhamento, Pais, Municipios, UF, Deslocamento, Agentes,
    Nomes)
from ...utils import timer

#
# SQL procedures
#
use_sqlite = True if env.get('SQL_DRIVER', 'sqlite') == 'sqlite' else False


def dummy(field, id_projeto, *args):
    return getattr(Custos, field)


ano_projeto = Projeto.AnoProjeto
sequencial = Projeto.Sequencial
id_projeto = Projeto.idProjeto
procs = func.sac.dbo


# Valores da proposta
if not use_sqlite:
    valor_proposta_base = procs.fnValorDaProposta(id_projeto)
    valor_solicitado = procs.fnValorSolicitado(id_projeto, sequencial)
    valor_aprovado = procs.fnValorAprovado(id_projeto, sequencial)
    valor_aprovado_convenio = procs.fnValorAprovadoConvenio(id_projeto,
                                                            sequencial)
    custo_projeto = procs.fnCustoProjeto(id_projeto, sequencial)
    outras_fontes = procs.fnOutrasFontes(id_projeto)
else:
    valor_proposta_base = dummy('valor_proposta', id_projeto)
    valor_solicitado = dummy('valor_solicitado', id_projeto, sequencial)
    valor_aprovado = dummy('valor_aprovado', id_projeto, sequencial)
    valor_aprovado_convenio = dummy('valor_aprovado_convenio', id_projeto,
                                    sequencial)
    custo_projeto = dummy('custo_projeto', id_projeto, sequencial)
    outras_fontes = dummy('outras_fontes', id_projeto)

# Valores derivados
_mecanismo = Projeto.Mecanismo
_mecanismos_convenio = or_(_mecanismo == '2', _mecanismo == '6')

valor_aprovado = case(
    [(_mecanismos_convenio, valor_aprovado_convenio)],
    else_=valor_aprovado,
)

valor_projeto = case(
    [(_mecanismos_convenio, valor_aprovado_convenio)],
    else_=valor_aprovado + outras_fontes,
)

valor_proposta = coalesce(valor_proposta_base, valor_solicitado)


#
# Query classes
#


class ProjetoQuery(Query):
    labels_to_fields = {
        # Projeto
        'nome': Projeto.NomeProjeto,
        'providencia': Projeto.ProvidenciaTomada,
        'PRONAC': Projeto.PRONAC,
        'UF': Projeto.UfProjeto,
        'data_inicio': Projeto.data_inicio_execucao,
        'data_inicio_min': Projeto.data_inicio_execucao,
        'data_inicio_max': Projeto.data_inicio_execucao,
        'data_termino': Projeto.data_fim_execucao,
        'data_termino_min': Projeto.data_fim_execucao,
        'data_termino_max': Projeto.data_fim_execucao,
        'IdPRONAC': Projeto.IdPRONAC,
        'ano_projeto': Projeto.AnoProjeto,

        # Pre-projeto
        'acessibilidade': PreProjeto.Acessibilidade,
        'objetivos': PreProjeto.Objetivos,
        'justificativa': PreProjeto.Justificativa,
        'democratizacao': PreProjeto.DemocratizacaoDeAcesso,
        'etapa': PreProjeto.EtapaDeTrabalho,
        'ficha_tecnica': PreProjeto.FichaTecnica,
        'resumo': PreProjeto.ResumoDoProjeto,
        'sinopse': PreProjeto.Sinopse,
        'impacto_ambiental': PreProjeto.ImpactoAmbiental,
        'especificacao_tecnica': PreProjeto.EspecificacaoTecnica,
        'estrategia_execucao': PreProjeto.EstrategiadeExecucao,

        # Interessado
        'municipio': Interessado.Cidade,
        'proponente': Interessado.Nome,
        'cgccpf': Interessado.CgcCpf,

        # Info
        'area': Area.Descricao,
        'segmento': Segmento.Descricao,
        'situacao': Situacao.Descricao,
        'mecanismo': Mecanismo.Descricao,

        # Derived info
        'enquadramento': Enquadramento.enquadramento,
        'valor_solicitado': valor_solicitado,
        'outras_fontes': outras_fontes,
        'valor_captado': custo_projeto,
        'valor_proposta': valor_proposta,
        'valor_aprovado': valor_aprovado,
        'valor_projeto': valor_projeto,
    }

    fields_already_filtered = {'data_inicio', 'data_termino'}

    @property
    def query_fields(self):
        black_list = {'data_inicio_min', 'data_inicio_max', 'data_termino_min', 'data_termino_max'}
        return tuple(v.label(k) for k, v in self.labels_to_fields.items() if k not in black_list)

    #
    # Queries
    #
    def query(self, limit=1, offset=0, data_inicio=None, data_inicio_min=None,
            data_inicio_max=None, data_termino=None, data_termino_min=None,
            data_termino_max=None, **kwargs):

        if(kwargs.get('PRONAC')):
            self.check_pronac(kwargs.get('PRONAC'))

        with timer('query projetos_list'):
            # Prepare query
            query = self.raw_query(*self.query_fields)
            query = (
                query
                .join(PreProjeto)
                .join(Interessado)
                .join(Area)
                .join(Segmento)
                .join(Situacao)
                .join(Mecanismo, Mecanismo.Codigo == Projeto.Mecanismo)
                .outerjoin(Enquadramento,
                           Enquadramento.IdPRONAC == Projeto.IdPRONAC))

            # For sqlite use
            if use_sqlite:
                query = query.join(Custos, Custos.IdPRONAC == Projeto.IdPRONAC)

            # # Filter query by dates
            end_of_day = (lambda x: None if x is None else x + ' 23:59:59')
            if data_inicio_min is not None:
                query = query.filter(Projeto.data_inicio_execucao >= data_inicio_min)

            if data_inicio_max is not None:
                query = query.filter(Projeto.data_inicio_execucao <= end_of_day(data_inicio_max))

            if data_termino_min is not None:
                query = query.filter(Projeto.data_fim_execucao >= data_termino_min)

            if data_termino_max is not None:
                query = query.filter(Projeto.data_fim_execucao <= end_of_day(data_termino_max))

        return query

    def check_pronac(self, pronac):
        try:
            int(pronac)
        except ValueError:
            result = {
                'message': 'PRONAC must be an integer',
                'message_code': 10
            }
            raise InvalidResult(result, status_code=404)

    # FIXME: using SQL procedure SAC.dbo.paDocumentos #permission denied
    def attached_documents(self, pronac_id):
        if not use_sqlite:
            query = text('SAC.dbo.paDocumentos :idPronac')
            return self.execute_query(query, {'idPronac': pronac_id}).fetchall()
        else:
            return []

    def attached_brands(self, idPronac):
        query = self.raw_query(Arquivo.idArquivo.label('id_arquivo'))

        query = (
            query
            .select_from(ArquivoImagem)
            .join(Arquivo, Arquivo.idArquivo == ArquivoImagem.idArquivo)
            .join(Documento, Documento.idArquivo == Arquivo.idArquivo)
            .join(DocumentoProjeto, DocumentoProjeto.idDocumento == Documento.idDocumento)
            .join(Projeto, DocumentoProjeto.idPronac == Projeto.IdPRONAC)
            .filter(DocumentoProjeto.idTipoDocumento == 1, Projeto.IdPRONAC == idPronac)
        )

        return query

    def postpone_request(self, idPronac):  # noqa: N804
        query = self.raw_query(
            Prorrogacao.DtPedido.label("data_pedido"),
            Prorrogacao.DtInicio.label("data_inicio"),
            Prorrogacao.DtFinal.label("data_final"),
            Prorrogacao.Observacao.label("observacao"),
            Prorrogacao.Atendimento.label("atendimento"),
            Usuarios.usu_nome.label("usuario"),
            case([
                (Prorrogacao.Atendimento == 'A', 'Em analise'),
                (Prorrogacao.Atendimento == 'N', 'Deferido'),
                (Prorrogacao.Atendimento == 'I', 'Indeferido'),
                (Prorrogacao.Atendimento == 'S', 'Processado'),
            ]).label("estado"),
        )
        query = (
            query
            .select_from(Prorrogacao)
            .join(Usuarios, Prorrogacao.Logon == Usuarios.usu_codigo)
            .filter(Prorrogacao.idPronac == idPronac)
        )

        return query

    def payments_listing(self, limit=None, offset=None, **kwargs):
        query_fields = (
            PlanilhaItens.Descricao.label('nome'),
            Comprovante.idComprovantePagamento
                        .label('id_comprovante_pagamento'),
            ComprovanteAprovacao.idPlanilhaAprovacao
                                .label('id_planilha_aprovacao'),
            Agentes.CNPJCPF.label('cgccpf'),
            Nomes.Descricao.label('nome_fornecedor'),
            Comprovante.DtPagamento.label('data_aprovacao'),

            case([
                (Comprovante.tpDocumento == '1', 'Boleto Bancario'),
                (Comprovante.tpDocumento == '2', 'Cupom Fiscal'),
                (Comprovante.tpDocumento == '3', 'Guia de Recolhimento'),
                (Comprovante.tpDocumento == '4', 'Nota Fiscal/Fatura'),
                (Comprovante.tpDocumento == '5', 'Recibo de Pagamento'),
                (Comprovante.tpDocumento == '6', 'RPA'),
            ]).label('tipo_documento'),
            Comprovante.nrComprovante.label('nr_comprovante'),
            Comprovante.dtEmissao.label('data_pagamento'),

            case([
                (Comprovante.tpFormaDePagamento == '1', 'Cheque'),
                (Comprovante.tpFormaDePagamento == '2', 'Transferencia Bancaria'),
                (Comprovante.tpFormaDePagamento == '3', 'Saque/Dinheiro'),
            ]).label('tipo_forma_pagamento'),
            Comprovante.nrDocumentoDePagamento.label('nr_documento_pagamento'),
            ComprovanteAprovacao.vlComprovado.label('valor_pagamento'),
            Comprovante.idArquivo.label('id_arquivo'),
            Comprovante.dsJustificativa.label('justificativa'),
            Arquivo.nmArquivo.label('nm_arquivo'),
        )

        if not kwargs.get('idPronac'):
            query_fields = query_fields + (Projeto.PRONAC.label('PRONAC'),)

        query = self.raw_query(*query_fields)
        query = query.select_from(ComprovanteAprovacao)

        query = (query
                .join(Comprovante,
                    ComprovanteAprovacao.idComprovantePagamento ==
                    Comprovante.idComprovantePagamento)
                .outerjoin(PlanilhaAprovacao,
                    PlanilhaAprovacao.idPlanilhaAprovacao ==
                    ComprovanteAprovacao.idPlanilhaAprovacao)
                .outerjoin(PlanilhaItens,
                    PlanilhaItens.idPlanilhaItens ==
                    PlanilhaAprovacao.idPlanilhaItem)
                .outerjoin(Nomes,
                    Nomes.idAgente == Comprovante.idFornecedor)
                .outerjoin(Arquivo,
                    Arquivo.idArquivo == Comprovante.idArquivo)
                .outerjoin(Agentes,
                    Agentes.idAgente == Comprovante.idFornecedor))

        if not kwargs.get('idPronac'):
            query = (query
                .join(Projeto,
                      Projeto.IdPRONAC == PlanilhaAprovacao.idPronac)
                .filter(Agentes.CNPJCPF.like(kwargs.get('cgccpf'))))
        else:
            query = (query
                .filter(PlanilhaAprovacao.idPronac == kwargs.get('idPronac')))

        query = query.order_by(Comprovante.dtEmissao)
        if(limit):
            query = query.limit(limit)
        if(offset):
            query = query.offset(offset)

        return query

    def taxing_report(self, idPronac):  # noqa: N803
        # Relatório fisco

        qtd_programada = PlanilhaAprovacao.qtItem * PlanilhaAprovacao.nrOcorrencia
        valor_programado = PlanilhaAprovacao.qtItem * PlanilhaAprovacao.nrOcorrencia * PlanilhaAprovacao.vlUnitario

        query_fields = (
            PlanilhaEtapa.idPlanilhaEtapa.label('id_planilha_etapa'),
            PlanilhaEtapa.Descricao.label('etapa'),
            PlanilhaItens.Descricao.label('item'),
            PlanilhaUnidade.Descricao.label('unidade'),
            qtd_programada.label('qtd_programada'),
            valor_programado.label('valor_programado'),

            case([(valor_programado == 0, 'NULL')],
                else_=func.round(func.sum(Comprovante.vlComprovacao) /
                valor_programado * 100, 2)).label('perc_executado'),

            case([(valor_programado == 0, 'NULL')],
                else_=func.round(100 - (func.sum(Comprovante.vlComprovacao) /
                valor_programado * 100), 2)).label('perc_a_executar'),

            func.sum(Comprovante.vlComprovacao).label('valor_executado')
        )

        query = self.raw_query(*query_fields)
        query = query.select_from(ComprovanteAprovacao)

        query = (query
                 .join(Comprovante,
                       ComprovanteAprovacao.idComprovantePagamento ==
                       Comprovante.idComprovantePagamento)
                 .join(PlanilhaAprovacao,
                       ComprovanteAprovacao.idPlanilhaAprovacao == PlanilhaAprovacao.idPlanilhaAprovacao)
                 .join(PlanilhaItens,
                       PlanilhaAprovacao.idPlanilhaItem == PlanilhaItens.idPlanilhaItens)
                 .join(PlanilhaEtapa,
                       PlanilhaAprovacao.idEtapa == PlanilhaEtapa.idPlanilhaEtapa)
                 .join(PlanilhaUnidade,
                       PlanilhaAprovacao.idUnidade == PlanilhaUnidade.idUnidade)
                 )

        query = query.filter(PlanilhaAprovacao.idPronac == idPronac)

        query = query.group_by(
            PlanilhaAprovacao.idPronac,
            PlanilhaEtapa.Descricao,
            PlanilhaItens.Descricao,
            PlanilhaUnidade.Descricao,
            PlanilhaAprovacao.qtItem,
            PlanilhaAprovacao.nrOcorrencia,
            PlanilhaAprovacao.vlUnitario,
            PlanilhaEtapa.idPlanilhaEtapa,
        )

        return query

    def goods_capital_listing(self, idPronac):
        # Relacao de bens de capital

        query_fields = (
            Comprovante.tpDocumentoLabel.label('Titulo'),
            Comprovante.nrComprovante.label('numero_comprovante'),
            PlanilhaItens.Descricao.label('Item'),
            Comprovante.dtEmissao.label('dtPagamento'),
            ItemCusto.dsItemDeCusto.label('Especificacao'),
            ItemCusto.dsMarca.label('Marca'),
            ItemCusto.dsFabricante.label('Fabricante'),
            (PlanilhaAprovacao.qtItem * PlanilhaAprovacao.nrOcorrencia).label('Qtde'),
            PlanilhaAprovacao.vlUnitario.label('valor_unitario'),
            (PlanilhaAprovacao.qtItem * PlanilhaAprovacao.nrOcorrencia * PlanilhaAprovacao.vlUnitario).label('valor_total'),
        )

        query = self.raw_query(*query_fields)
        query = query.select_from(ComprovanteAprovacao)
        query = (query
                 .join(Comprovante,
                       ComprovanteAprovacao.idComprovantePagamento ==
                       Comprovante.idComprovantePagamento)
                 .join(PlanilhaAprovacao,
                       ComprovanteAprovacao.idPlanilhaAprovacao == PlanilhaAprovacao.idPlanilhaAprovacao)
                 .join(PlanilhaItens,
                       PlanilhaAprovacao.idPlanilhaItem == PlanilhaItens.idPlanilhaItens)
                 .join(ItemCusto,
                       PlanilhaAprovacao.idPlanilhaAprovacao == ItemCusto.idPlanilhaAprovacao)
                 )
        query = query.filter(PlanilhaAprovacao.idPronac == idPronac)

        return query


class CaptacaoQuery(Query):
    """
    Returns Captacao value of a project
    """
    def query(self, PRONAC):  # noqa: N803
        query = self.raw_query(
            Captacao.PRONAC,
            Captacao.CaptacaoReal.label('valor'),
            Captacao.data_recibo.label('data_recibo'),
            Captacao.CgcCpfMecena.label('cgccpf'),
            Projeto.NomeProjeto.label('nome_projeto'),
            Interessado.Nome.label('nome_doador'),
        )
        query = (
            query
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
            .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
        )
        return filter_query(query, {Captacao.PRONAC: PRONAC})


class AreaQuery(Query):
    """
    Returns description and id of Area
    """
    def query(self):
        return self.select_as(Area, Descricao='nome', Codigo='codigo')


class SegmentoQuery(Query):
    """
    Returns description and id of Segmento
    """
    def query(self):
        return self.select_as(Segmento, Descricao='nome', Codigo='codigo')


class CertidoesNegativasQuery(Query):
    """
    Returns certificate's name and situation according to it's id
    """
    @property
    def descricao(self):
        code = CertidoesNegativas.CodigoCertidao
        return case([
            (code == '49', 'Quitação de Tributos Federais'),
            (code == '51', 'FGTS'),
            (code == '52', 'INSS'),
            (code == '244', 'CADIN'),
        ])

    @property
    def situacao(self):
        return case(
            [(CertidoesNegativas.cdSituacaoCertidao == 0, 'Pendente')],
            else_='Não Pendente'
        )

    def query(self, **kwargs):  # noqa: N803
        query = self.raw_query(
            CertidoesNegativas.data_emissao.label('data_emissao'),
            CertidoesNegativas.data_validade.label('data_validade'),
            self.descricao.label('descricao'),
            self.situacao.label('situacao'),
        )

        if kwargs.get('PRONAC'):
            PRONAC = kwargs.get('PRONAC')
            query = query.filter(CertidoesNegativas.PRONAC == PRONAC)

        return query


class DivulgacaoQuery(Query):
    """
    Returns instrument of propagation and its type. Ex: Peça - CARTAZ/POSTER,
    Veiculo - IMPRESSOS
    """
    def query(self, PRONAC):
        verificacao_peca = alias(Verificacao, name='verificacao_peca')
        verificacao_veiculo = alias(Verificacao, name='verificacao_veiculo')

        query = (self.raw_query(
            verificacao_peca.c.Descricao.label('peca'),
            verificacao_veiculo.c.Descricao.label('veiculo'))
        .select_from(PlanoDivulgacao)
        .join(Projeto, Projeto.idProjeto == PlanoDivulgacao.idProjeto)
        .join(verificacao_peca,
              verificacao_peca.c.idVerificacao == PlanoDivulgacao.idPeca)
        .join(verificacao_veiculo,
              verificacao_veiculo.c.idVerificacao == PlanoDivulgacao.idVeiculo)
        .filter(and_(Projeto.PRONAC == PRONAC,
                PlanoDivulgacao.stPlanoDivulgacao == 1)))

        return query


class DeslocamentoQuery(Query):
    """
    Returns descriptions of places which the project may pass.
    """
    def query(self, PRONAC):  # noqa: N803
        pais_origem = alias(Pais, name='pais_origem')
        pais_destino = alias(Pais, name='pais_destino')
        uf_origem = alias(UF, name='uf_origem')
        uf_destino = alias(UF, name='uf_destino')
        municipio_origem = alias(Municipios, name='municipios_origem')
        municipio_destino = alias(Municipios, name='municipios_destino')

        query = self.raw_query(
            Deslocamento.idDeslocamento.label("id_deslocamento"),
            Deslocamento.idProjeto.label("id_projeto"),
            pais_origem.c.Descricao.label("PaisOrigem"),
            pais_destino.c.Descricao.label("PaisDestino"),
            uf_origem.c.Descricao.label("UFOrigem"),
            uf_destino.c.Descricao.label("UFDestino"),
            municipio_origem.c.Descricao.label("MunicipioOrigem"),
            municipio_destino.c.Descricao.label("MunicipioDestino"),
            Deslocamento.Qtde.label("Qtde"),
        )

        query = (
            query
            .select_from(Deslocamento)
            .join(Projeto, Projeto.idProjeto == Deslocamento.idProjeto)

            .join(pais_origem, pais_origem.c.idPais == Deslocamento.idPaisOrigem)
            .join(pais_destino, pais_destino.c.idPais == Deslocamento.idPaisDestino)

            .join(uf_origem, uf_origem.c.iduf == Deslocamento.idUFOrigem)
            .join(uf_destino, uf_destino.c.iduf == Deslocamento.idUFDestino)

            .join(municipio_origem, municipio_origem.c.idMunicipioIBGE == Deslocamento.idMunicipioOrigem)
            .join(municipio_destino, municipio_destino.c.idMunicipioIBGE == Deslocamento.idMunicipioDestino)

            .filter(Projeto.PRONAC == PRONAC)
        )

        return self.execute_query(query, {'PRONAC': PRONAC}).fetchall()


class DistribuicaoQuery(Query):
    """
    Returns information of how the project will be distributed. Ex: ticket prices...
    """
    def query(self, PRONAC):  # noqa: N803
        return (
            self.raw_query(
                PlanoDistribuicao.idPlanoDistribuicao.label('idPlanoDistribuicao'),
                PlanoDistribuicao.QtdeVendaNormal.label('QtdeVendaNormal'),
                PlanoDistribuicao.QtdeVendaPromocional.label('QtdeVendaPromocional'),
                PlanoDistribuicao.PrecoUnitarioNormal.label('PrecoUnitarioNormal'),
                PlanoDistribuicao.PrecoUnitarioPromocional.label('PrecoUnitarioPromocional'),
                PlanoDistribuicao.QtdeOutros.label('QtdeOutros'),
                PlanoDistribuicao.QtdeProponente.label('QtdeProponente'),
                PlanoDistribuicao.QtdeProduzida.label('QtdeProduzida'),
                PlanoDistribuicao.QtdePatrocinador.label('QtdePatrocinador'),
                Area.Descricao.label('area'),
                Segmento.Descricao.label('segmento'),
                Produto.Descricao.label('produto'),
                Verificacao.Descricao.label('posicao_logo'),
                Projeto.Localizacao.label('Localizacao'),
            )
            .join(Projeto)
            .join(Produto)
            .join(Area, Area.Codigo == PlanoDistribuicao.Area)
            .join(Segmento, Segmento.Codigo == PlanoDistribuicao.Segmento)
            .join(Verificacao)
            .filter(and_(Projeto.PRONAC == PRONAC,
                         PlanoDistribuicao.stPlanoDistribuicaoProduto == 1))
        )


class ReadequacaoQuery(Query):
    def query(self, IdPRONAC):  # noqa: N803
        query = self.raw_query(
            Readequacao.idReadequacao.label("id_readequacao"),
            Readequacao.dtSolicitacao.label("data_solicitacao"),
            cast(Readequacao.dsSolicitacao, Text).label("descricao_solicitacao"),
            cast(Readequacao.dsJustificativa, Text).label("descricao_justificativa"),
            Readequacao.idSolicitante.label("id_solicitante"),
            Readequacao.idAvaliador.label("id_avaliador"),
            Readequacao.dtAvaliador.label("data_avaliador"),
            cast(Readequacao.dsAvaliacao, Text).label("descricao_avaliacao"),
            Readequacao.idTipoReadequacao.label("id_tipo_readequacao"),
            cast(TipoReadequacao.dsReadequacao, Text).label("descricao_readequacao"),
            Readequacao.stAtendimento.label("st_atendimento"),
            Readequacao.siEncaminhamento.label("si_encaminhamento"),
            cast(TipoEncaminhamento.dsEncaminhamento, Text).label("descricao_encaminhamento"),
            Readequacao.stEstado.label("st_estado"),
            Arquivo.idArquivo.label("id_arquivo"),
            Arquivo.nmArquivo.label("nome_arquivo")
        )

        query = (
            query
            .select_from(Readequacao)
            .join(TipoEncaminhamento,
                  Readequacao.siEncaminhamento ==
                  TipoEncaminhamento.idTipoEncaminhamento)
            .join(TipoReadequacao,
                  TipoReadequacao.idTipoReadequacao ==
                  Readequacao.idTipoReadequacao)
            .outerjoin(Documento,
                       Documento.idDocumento == Readequacao.idDocumento)
            .outerjoin(Arquivo, Arquivo.idArquivo == Documento.idArquivo)
            .filter(Readequacao.IdPRONAC == IdPRONAC)
            .filter(Readequacao.siEncaminhamento != 12))

        return query
