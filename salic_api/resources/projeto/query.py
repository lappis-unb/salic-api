import operator

from os import environ as env
from sqlalchemy import case, func, and_, or_, cast, Text
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import desc, alias
from sqlalchemy.sql.functions import coalesce

from salic_api.models import PlanoDivulgacao
from .raw_sql import payments_listing_sql, normalize_sql
from ..query import Query, filter_query, filter_query_like
from ..serialization import listify_queryset
from ...models import (
    ComprovantePagamento as Comprovante, PlanilhaItens, PlanilhaAprovacao,
    ComprovantePagamentoxPlanilhaAprovacao as ComprovanteAprovacao, ItemCusto,
    PlanilhaEtapa, PlanilhaUnidade,
    Projeto, Interessado, Situacao, Enquadramento, PreProjeto,
    Captacao, CertidoesNegativas, Verificacao, PlanoDistribuicao, Produto, Area,
    Segmento, Custos, Mecanismo, Arquivo, ArquivoImagem, Documento,
    DocumentoProjeto, Prorrogacao, Usuarios, Readequacao, TipoReadequacao,
    TipoEncaminhamento, Pais, Municipios, UF, Deslocamento)
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
        'data_termino': Projeto.data_fim_execucao,
        'IdPRONAC': Projeto.IdPRONAC,
        'ano_projeto': Projeto.AnoProjeto,

        ## Pre-projeto
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

        ## Interessado
        'municipio': Interessado.Cidade,
        'proponente': Interessado.Nome,
        'cgccpf': Interessado.CgcCpf,

        ## Info
        'area': Area.Descricao,
        'segmento': Segmento.Descricao,
        'situacao': Situacao.Descricao,
        'mecanismo': Mecanismo.Descricao,

        ## Derived info
        'enquadramento': Enquadramento.enquadramento,
        'valor_solicitado': valor_solicitado, #permission denied
        'outras_fontes': outras_fontes, #permission denied
        'valor_captado': custo_projeto,
        'valor_proposta': valor_proposta, #permission denied
        'valor_aprovado': valor_aprovado, #permission denied
        'valor_projeto': valor_projeto, #permission denied
        # TODO When fix uncomment tests/examples.py lines 196, 203, 205, 206 and 207
    }

    fields_already_filtered = {'data_inicio','data_termino'}
    #
    # Queries
    #
    def query(self, limit=1, offset=0, data_inicio=None, data_inicio_min=None,
        data_inicio_max=None, data_termino=None, data_termino_min=None,
        data_termino_max=None, **kwargs):
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
                .join(Mecanismo,
                    Mecanismo.Codigo == Projeto.Mecanismo)
                .outerjoin(Enquadramento,
                    Enquadramento.IdPRONAC == Projeto.IdPRONAC)
                )

            # For sqlite use
            if use_sqlite:
                query = query.join(Custos,
                        Custos.IdPRONAC == Projeto.IdPRONAC)

            # # Filter query by dates
            end_of_day = (lambda x: None if x is None else x + ' 23:59:59')
            query = filter_query(query, {
                Projeto.data_inicio_execucao: data_inicio or data_inicio_min,
                Projeto.data_fim_execucao: data_termino or data_termino_min,
            }, op=operator.ge)

            query = filter_query(query, [
                (Projeto.data_inicio_execucao, end_of_day(data_inicio)),
                (Projeto.data_inicio_execucao, end_of_day(data_inicio_max)),
                (Projeto.data_inicio_execucao, end_of_day(data_termino)),
                (Projeto.data_fim_execucao, end_of_day(data_termino_max)),
            ], op=operator.le)

        return query

   #  FIXME: using SQL procedure SAC.dbo.paDocumentos #permission denied
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
            .filter(DocumentoProjeto.idTipoDocumento==1, Projeto.IdPRONAC==idPronac)
        )

        return self.execute_query(query, {'IdPRONAC': idPronac}).fetchall()

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
            .filter(Prorrogacao.idPronac==idPronac)
        )

        return self.execute_query(query, {'IdPRONAC': idPronac}).fetchall()

    def payments_listing(self, limit=None, offset=None, idPronac=None,
                         cgccpf=None):
        params = {'offset': offset, 'limit': limit}
        if idPronac:
            params['idPronac'] = idPronac
        else:
            params['cgccpf'] = '%{}%'.format(cgccpf)
        query = payments_listing_sql(idPronac, limit is not None)
        return self.execute_query(query, params).fetchall()

    #def payments_listing_count(self, idPronac=None, cgccpf=None):  # noqa: N803
    #    if idPronac is not None:
    #        query = text(normalize_sql("""
    #                SELECT
    #                    COUNT(b.idArquivo) AS total

    #                    FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
    #                    INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
    #                    LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
    #                    LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
    #                    LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
    #                    LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
    #                    LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (c.idPronac = :idPronac)
    #                """))
    #        params = {'idPronac': idPronac}
    #        result = self.execute_query(query, params).fetchall()

    #    else:
    #        query = text(normalize_sql("""
    #                SELECT
    #                    COUNT(b.idArquivo) AS total

    #                    FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
    #                    INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
    #                    LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
    #                    LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
    #                    LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
    #                    LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
    #                    JOIN SAC.dbo.Projetos AS Projetos ON c.idPronac = Projetos.IdPRONAC
    #                    LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (g.CNPJCPF LIKE :cgccpf)
    #                """))

    #        params = {'cgccpf': '%' + cgccpf + '%'}
    #        result = self.execute_query(query, params).fetchall()

    #    n_records = listify_queryset(result)
    #    return n_records[0]['total']

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
                else_ = func.round(func.sum(Comprovante.vlComprovacao) / valor_programado * 100, 2)
            ).label('perc_executado'),

            case([(valor_programado == 0, 'NULL')],
                else_ = func.round(100 - (func.sum(Comprovante.vlComprovacao) / valor_programado * 100), 2)
            ).label('perc_a_executar'),

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

    def query(self, PRONAC=None, CgcCpf=None):  # noqa: N803
        query = self.raw_query(
            CertidoesNegativas.data_emissao.label('data_emissao'),
            CertidoesNegativas.data_validade.label('data_validade'),
            self.descricao.label('descricao'),
            self.situacao.label('situacao'),
        )
        return filter_query(query, {CertidoesNegativas.PRONAC: PRONAC})


class DivulgacaoQuery(Query):
    """
    Returns instrument of propagation and its type. Ex: Peça - CARTAZ/POSTER,
    Veiculo - IMPRESSOS
    """
    def query(self, IdPRONAC):
        query = (self.raw_query(
            Verificacao.Descricao.label('peca'),
            Verificacao.Descricao.label('veiculo'),
        ).select_from(PlanoDivulgacao)
         .join(Projeto, Projeto.idProjeto == PlanoDivulgacao.idProjeto)
         .join(Verificacao,
               Verificacao.idVerificacao == PlanoDivulgacao.idPeca or
               Verificacao.idVerificacao == PlanoDivulgacao.idVeiculo)
         .filter(and_(Projeto.IdPRONAC == IdPRONAC,
                      PlanoDivulgacao.stPlanoDivulgacao == 1))
        )

        return query


class DeslocamentoQuery(Query):
    """
    Returns descriptions of places which the project may pass.
    """
    def query(self, IdPRONAC):  # noqa: N803
        pais_origem = alias(Pais,name='pais_origem')
        pais_destino = alias(Pais,name='pais_destino')
        uf_origem = alias(UF,name='uf_origem')
        uf_destino = alias(UF,name='uf_destino')
        municipio_origem = alias(Municipios,name='municipios_origem')
        municipio_destino = alias(Municipios,name='municipios_destino')

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
            .join(Projeto, Projeto.idProjeto==Deslocamento.idProjeto)

            .join(pais_origem, pais_origem.c.idPais==Deslocamento.idPaisOrigem)
            .join(pais_destino, pais_destino.c.idPais==Deslocamento.idPaisDestino)

            .join(uf_origem, uf_origem.c.iduf==Deslocamento.idUFOrigem)
            .join(uf_destino, uf_destino.c.iduf==Deslocamento.idUFDestino)

            .join(municipio_origem, municipio_origem.c.idMunicipioIBGE==Deslocamento.idMunicipioOrigem)
            .join(municipio_destino, municipio_destino.c.idMunicipioIBGE==Deslocamento.idMunicipioDestino)

            .filter(Projeto.IdPRONAC == IdPRONAC)
        )

        return self.execute_query(query, {'IdPRONAC': IdPRONAC}).fetchall()


class DistribuicaoQuery(Query):
    """
    Returns information of how the project will be distributed. Ex: ticket prices...
    """
    def query(self, IdPRONAC):  # noqa: N803
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
            .filter(and_(Projeto.IdPRONAC == IdPRONAC,
                         PlanoDistribuicao.stPlanoDistribuicaoProduto == 0))
        )


class ReadequacaoQuery(Query):
    """

    """
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
                TipoEncaminhamento.idTipoEncaminhamento
            )
            .join(TipoReadequacao,
                TipoReadequacao.idTipoReadequacao ==
                Readequacao.idTipoReadequacao
            )
            .outerjoin(Documento,
                    Documento.idDocumento == Readequacao.idDocumento)
            .outerjoin(Arquivo, Arquivo.idArquivo == Documento.idArquivo)
            .filter(Readequacao.IdPRONAC == IdPRONAC)
            .filter(Readequacao.siEncaminhamento != 12)
        )

        return query

class AdequacoesPedidoQuery(Query):
    def query(self, IdPRONAC):  # noqa: N803
        return []  # FIXME

        stmt = text("""
            SELECT
                a.idReadequacao,
                a.idPronac,
                a.dtSolicitacao,
                CAST(a.dsSolicitacao AS TEXT) AS dsSolicitacao,
                CAST(a.dsJustificativa AS TEXT) AS dsJustificativa,
                a.idSolicitante,
                a.idAvaliador,
                a.dtAvaliador,
                CAST(a.dsAvaliacao AS TEXT) AS dsAvaliacao,
                a.idTipoReadequacao,
                CAST(c.dsReadequacao AS TEXT) AS dsReadequacao,
                a.stAtendimento,
                a.siEncaminhamento,
                CAST(b.dsEncaminhamento AS TEXT) AS dsEncaminhamento,
                a.stEstado,
                e.idArquivo,
                e.nmArquivo
             FROM SAC.dbo.tbReadequacao AS a
             INNER JOIN SAC.dbo.tbTipoEncaminhamento AS b ON a.siEncaminhamento = b.idTipoEncaminhamento INNER JOIN SAC.dbo.tbTipoReadequacao AS c ON c.idTipoReadequacao = a.idTipoReadequacao
             LEFT JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON d.idDocumento = a.idDocumento
             LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS e ON e.idArquivo = d.idArquivo WHERE (a.idPronac = :IdPRONAC) AND (a.siEncaminhamento <> 12)
            """)
        return self.execute_query(stmt, {'IdPRONAC': IdPRONAC})


class AdequacoesParecerQuery(Query):
    def query(self, IdPRONAC):  # noqa: N803
        return []  # FIXME

        stmt = text("""
            SELECT
                a.idReadequacao,
                a.idPronac,
                a.dtSolicitacao,
                CAST(a.dsSolicitacao AS TEXT) AS dsSolicitacao,
                CAST(a.dsJustificativa AS TEXT) AS dsJustificativa,
                a.idSolicitante,
                a.idAvaliador,
                a.dtAvaliador,
                CAST(a.dsAvaliacao AS TEXT) AS dsAvaliacao,
                a.idTipoReadequacao,
                CAST(c.dsReadequacao AS TEXT) AS dsReadequacao,
                a.stAtendimento,
                a.siEncaminhamento,
                CAST(b.dsEncaminhamento AS TEXT) AS dsEncaminhamento,
                a.stEstado,
                e.idArquivo,
                e.nmArquivo
            FROM tbReadequacao AS a
            INNER JOIN SAC.dbo.tbTipoEncaminhamento AS b ON a.siEncaminhamento = b.idTipoEncaminhamento
            INNER JOIN SAC.dbo.tbTipoReadequacao AS c ON c.idTipoReadequacao = a.idTipoReadequacao
            LEFT JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON d.idDocumento = a.idDocumento
            LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS e ON e.idArquivo = d.idArquivo WHERE (a.idPronac = :IdPRONAC) AND (a.siEncaminhamento <> 12)
        """)
        return self.execute_query(stmt, {'IdPRONAC': IdPRONAC})
