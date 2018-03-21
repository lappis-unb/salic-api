from os import environ as env
from sqlalchemy import Column, Date, DateTime, Integer, String, DATE, func, \
    VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# TODO: can we support the money type in the SQL Server?
Money = String
use_sqlite = True if env.get('SQL_DRIVER', 'sqlite') == 'sqlite' else False

if use_sqlite:
    DateTime = Date  # noqa: F811
    date_column = (lambda x: func.cast(x, VARCHAR))
else:
    date_column = (lambda x: func.cast(x, DATE))


# FIXME put right columns when given access to this table

def table_name(name):
    if use_sqlite:
        return name.rpartition('.')[-1]
    else:
        return name

def foreign_key(table,column):
    return '{}.{}'.format(table.__tablename__, column)

# FIXME put right columns when given access to this table.
# for now using made up primary key
class Prorrogacao(Base):
    """
    Contem a data de início e de fim da projeto
    (???.???.prorrogacao)
    """
    __tablename__ = table_name('prorrogacao')

    idProrrogacao = Column(Integer, primary_key=True)
    Logon = Column(Integer)
    DtPedido = Column(DateTime)
    DtInicio = Column(DateTime)
    DtFinal = Column(DateTime)
    Observacao = Column(String)
    Atendimento = Column(String)
    idPronac = Column(Integer)


class ItemCustoBase:
    __tablename__ = table_name('BDCORPORATIVO.scSAC.tbItemCusto')


class ComprovantePagamentoxPlanilhaAprovacaoBase:  # noqa: N801
    __tablename__ = table_name('BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao')


class ComprovantePagamentoBase:  # noqa: N801
    __tablename__ = table_name('BDCORPORATIVO.scSAC.tbComprovantePagamento')


class ArquivoBase:  # noqa: N801
    __tablename__=table_name('BDCORPORATIVO.scCorp.tbArquivo')


class ArquivoImagemBase:
    __tablename__=table_name('BDCORPORATIVO.scCorp.tbArquivoImagem')


class DocumentoBase:
    __tablename__=table_name('BDCORPORATIVO.scCorp.tbDocumento')


class DocumentoProjetoBase:
    __tablename__=table_name('BDCORPORATIVO.scCorp.tbDocumentoProjeto')


class NomesBase:
    __tablename__ = table_name('Agentes.dbo.Nomes')


class AgentesBase:
    __tablename__ = table_name('Agentes.dbo.Agentes')


class InternetBase:
    __tablename__ = table_name('Agentes.dbo.Internet')


class PaisBase:
    __tablename__ = table_name('Agentes.dbo.Pais')


class UFBase:
    __tablename__ = table_name('Agentes.dbo.uf')


class MunicipiosBase:
    __tablename__ = table_name('Agentes.dbo.Municipios')


class SegmentoBase:
    __tablename__ = table_name('SAC.dbo.Segmento')


class SituacaoBase:
    __tablename__ = table_name('SAC.dbo.Situacao')


class MecanismoBase:
    __tablename__ = table_name('SAC.dbo.Mecanismo')


class PreProjetoBase:
    __tablename__ = table_name('SAC.dbo.PreProjeto')


class EnquadramentoBase:
    __tablename__ = table_name('SAC.dbo.Enquadramento')


class AreaBase:
    __tablename__ = table_name('SAC.dbo.Area')


class InteressadoBase:
    __tablename__ = table_name('SAC.dbo.Interessado')


class CaptacaoBase:
    __tablename__ = table_name('sac.dbo.Captacao')


class CertidoesNegativasBase:
    __tablename__ = table_name('SAC.dbo.CertidoesNegativas')


class VerificacaoBase:
    __tablename__ = table_name('SAC.dbo.Verificacao')


class PlanoDivulgacaoBase:
    __tablename__ = table_name('SAC.dbo.PlanoDeDivulgacao')


class ProdutoBase:
    __tablename__ = table_name('SAC.dbo.Produto')


class PlanilhaItensBase:  # noqa: N801
    __tablename__ = table_name('SAC.dbo.tbPlanilhaItens')


class PlanilhaEtapaBase:
    __tablename__ = table_name('SAC.dbo.tbPlanilhaEtapa')


class PlanilhaUnidadeBase:
    __tablename__ = table_name('SAC.dbo.tbPlanilhaUnidade')


class ReadequacaoBase:
    __tablename__ = table_name('SAC.dbo.tbReadequacao')


class TipoReadequacaoBase:
    __tablename__ = table_name('SAC.dbo.tbTipoReadequacao')


class TipoEncaminhamentoBase:
    __tablename__ = table_name('SAC.dbo.tbTipoEncaminhamento')


class ProjetosBase:
    __tablename__ = table_name('sac.dbo.Projetos')


class PlanoDistribuicaoBase:
    __tablename__ = table_name('SAC.dbo.PlanoDistribuicaoProduto')


class PlanilhaAprovacaoBase:  # noqa: N801
    __tablename__ = table_name('SAC.dbo.tbPlanilhaAprovacao')


class DeslocamentoBase:
    __tablename__ = table_name('SAC.dbo.tbDeslocamento')


class UsuariosBase:
    __tablename__ = table_name('TABELAS.dbo.Usuarios')
