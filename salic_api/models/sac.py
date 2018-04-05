from sqlalchemy import Column, Integer, CHAR, String, Text, ForeignKey, case, \
    Boolean
from sqlalchemy.orm import column_property, relationship

from .base import *


class Segmento(SegmentoBase, Base):
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)

    # Values: 1 - Artigo 26 (30%), 2 - Artigo 18 (100%)
    tpEnquadramento = Column(CHAR)


class Situacao(SituacaoBase, Base):
    Codigo = Column(CHAR, primary_key=True)
    Descricao = Column(String)


class Mecanismo(MecanismoBase, Base):
    # Values:
    # 1 - Mecenato
    # 2 - FNC
    # The values bellow were removed from the database
    # 3 - Audiovisual (disabled)
    # 4 - Conversão da dívida externa (disabled)
    # 5 - Mecenato audiovisual (disabled)
    # 6 - Recurso do Tesouro
    # 7 - Outras fontes (disabled)
    Codigo = Column(CHAR, primary_key=True)
    Descricao = Column(String)


class PreProjeto(PreProjetoBase, Base):
    idPreProjeto = Column(Integer, primary_key=True)
    NomeProjeto = Column(String)
    DtInicioDeExecucao = Column(DateTime)
    data_inicio_execucao = date_column(DtInicioDeExecucao)
    DtFinalDeExecucao = Column(DateTime)
    data_final_execucao = date_column(DtFinalDeExecucao)
    dtAceite = Column(DateTime)
    data_aceite = date_column(dtAceite)
    DtArquivamento = Column(DateTime)
    data_arquivamento = date_column(DtArquivamento)
    Objetivos = Column(String)
    Justificativa = Column(String)
    Acessibilidade = Column(String)
    DemocratizacaoDeAcesso = Column(String)
    EtapaDeTrabalho = Column(String)
    FichaTecnica = Column(String)
    ResumoDoProjeto = Column(String)
    Sinopse = Column(String)
    ImpactoAmbiental = Column(String)
    EspecificacaoTecnica = Column(String)
    EstrategiadeExecucao = Column(String)

    # Original table does not use a foreign key constraint (possibly because
    # it uses the wrong data type in this column. The original table uses a
    # CHAR primary key).
    #
    # Values: 1 - Mecenato, 2 - FNC (maybe more...)
    Mecanismo = Column(Integer, ForeignKey(foreign_key(MecanismoBase, "Codigo")))

    # Related fields
    mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])


class Enquadramento(EnquadramentoBase, Base):
    IdEnquadramento = Column(Integer, primary_key=True)
    Enquadramento = Column(Integer)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    IdPRONAC = Column(Integer, ForeignKey('Projetos.IdPRONAC'))

    # Computed properties
    enquadramento = case(
        [
            (Enquadramento == 1, 'Artigo 26'),
            (Enquadramento == 2, 'Artigo 18'),
        ],
        else_='Nao enquadrado',
    ).label('enquadramento')


class Area(AreaBase, Base):
    Codigo = Column(String, primary_key=True)
    Descricao = Column(String)


class Interessado(InteressadoBase, Base):
    CgcCpf = Column(String, primary_key=True)
    Nome = Column(String)
    Responsavel = Column(String)
    Uf = Column(CHAR)
    Cidade = Column(String)
    tipoPessoa = Column(CHAR)

    # Related field
    captacao_related = relationship(
        'Captacao',
        primaryjoin='{}.CgcCpf=={}.CgcCpfMecena'.format(
            table_name('sac.dbo.Interessado'),
            table_name('sac.dbo.Captacao')),
    )
    projeto_related = relationship(
        'Projeto',
        primaryjoin='{}.CgcCpf=={}.CgcCpf'.format(
            table_name('sac.dbo.Interessado'),
            table_name('sac.dbo.Projeto')),
    )

    # Computed fields
    tipoPessoaLabel = case(
        [
            (tipoPessoa == '1', 'fisica'),
        ],
        else_='juridica'
    )


class Captacao(CaptacaoBase, Base):
    Idcaptacao = Column(Integer, primary_key=True)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    CaptacaoReal = Column(Money)
    DtRecibo = Column(DateTime)
    data_recibo = date_column(DtRecibo)
    CgcCpfMecena = Column(String, ForeignKey(foreign_key(InteressadoBase, "CgcCpf")))

    # Related fields
    interessado_related = relationship(
        'Interessado',
        foreign_keys=[CgcCpfMecena],
    )


class CertidoesNegativas(CertidoesNegativasBase, Base):
    idCertidoesNegativas = Column(Integer, primary_key=True)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    DtEmissao = Column(DateTime)
    data_emissao = date_column(DtEmissao)
    DtValidade = Column(DateTime)
    data_validade = date_column(DtValidade)
    CodigoCertidao = Column(Integer)
    cdSituacaoCertidao = Column(Integer)
    CgcCpf = Column(String, ForeignKey(foreign_key(InteressadoBase, "CgcCpf")))


class Verificacao(VerificacaoBase, Base):
    idVerificacao = Column(Integer, primary_key=True)
    idTipo = Column(Integer)
    Descricao = Column(String)
    stEstado = Column(Boolean)


class PlanoDivulgacao(PlanoDivulgacaoBase, Base):
    idPlanoDivulgacao = Column(Integer, primary_key=True)
    stPlanoDivulgacao = Column(Boolean)
    idPeca = Column(Integer, ForeignKey(foreign_key(VerificacaoBase, "idVerificacao")))
    idVeiculo = Column(Integer, ForeignKey(foreign_key(VerificacaoBase, "idVerificacao")))
    idProjeto = Column(Integer, ForeignKey(foreign_key(PreProjetoBase, "idPreProjeto")))

    # Related fields
    projeto_related = relationship('PreProjeto', foreign_keys=[idProjeto])


class Produto(ProdutoBase, Base):
    Codigo = Column(Integer, primary_key=True)
    Descricao = Column(String)
    Sintese = Column(Text)
    Idorgao = Column(Integer)
    stEstado = Column(Boolean)

    # Original table does not use a foreign key constraint
    Area = Column(CHAR, ForeignKey(foreign_key(AreaBase, "Codigo")))


class PlanilhaItens(PlanilhaItensBase, Base):  # noqa: N801
    idPlanilhaItens = Column(Integer, primary_key=True)
    Descricao = Column(String)


class PlanilhaEtapa(PlanilhaEtapaBase, Base):
    idPlanilhaEtapa = Column(Integer, primary_key=True)
    Descricao = Column(String)


class PlanilhaUnidade(PlanilhaUnidadeBase, Base):
    idUnidade = Column(Integer, primary_key=True)
    Descricao = Column(String)


class Readequacao(ReadequacaoBase, Base):
    idReadequacao = Column(Integer, primary_key=True)
    IdPRONAC = Column(Integer, ForeignKey(foreign_key(ProjetosBase, "IdPRONAC")))
    dtSolicitacao = Column(String)
    dsJustificativa = Column(String)
    idSolicitante = Column(Integer)
    idAvaliador = Column(Integer)
    dtAvaliador = Column(String)
    dsAvaliacao = Column(String)
    idTipoReadequacao = Column(Integer)
    dsReadequacao = Column(String)
    stAtendimento = Column(String)
    siEncaminhamento = Column(Integer)
    dsEncaminhamento = Column(String)
    dsSolicitacao = Column(String)
    stEstado = Column(String)
    idDocumento = Column(Integer, ForeignKey(foreign_key(DocumentoBase, "idDocumento")))


class TipoReadequacao(TipoReadequacaoBase, Base):
    idTipoReadequacao = Column(Integer, primary_key=True)
    dsReadequacao = Column(String)


class TipoEncaminhamento(TipoEncaminhamentoBase, Base):
    idTipoEncaminhamento = Column(Integer, primary_key=True)
    dsEncaminhamento = Column(String)


class Projeto(ProjetosBase, Base):
    IdPRONAC = Column(Integer, primary_key=True)
    AnoProjeto = Column(CHAR)
    Sequencial = Column(String)
    PRONAC = column_property(AnoProjeto + Sequencial)
    NomeProjeto = Column(String)
    Localizacao = Column(String)
    DtInicioExecucao = Column(DateTime)  # Date?
    data_inicio_execucao = date_column(DtInicioExecucao)
    DtFimExecucao = Column(DateTime)
    data_fim_execucao = date_column(DtFimExecucao)
    UfProjeto = Column(CHAR)
    SolicitadoReal = Column(Money)
    SolicitadoUfir = Column(Money)
    SolicitadoCusteioUfir = Column(Money)
    SolicitadoCusteioReal = Column(Money)
    SolicitadoCapitalUfir = Column(Money)
    SolicitadoCapitalReal = Column(Money)
    ResumoProjeto = Column(Text)
    ProvidenciaTomada = Column(String)
    Segmento = Column(String, ForeignKey(foreign_key(SegmentoBase, "Codigo")))
    Situacao = Column(CHAR, ForeignKey(foreign_key(SituacaoBase, "Codigo")))
    CgcCpf = Column(String, ForeignKey(foreign_key(InteressadoBase, "CgcCpf")))
    idProjeto = Column(Integer, ForeignKey(foreign_key(PreProjetoBase, "idPreProjeto")))

    # Original DB do not create a foreign key constraint
    Area = Column(CHAR, ForeignKey(foreign_key(AreaBase, "Codigo")))
    Mecanismo = Column(CHAR, ForeignKey(foreign_key(MecanismoBase, "Codigo")))

    # Related fields
    preprojeto_related = relationship("PreProjeto", foreign_keys=[idProjeto])
    situacao_related = relationship("Situacao", foreign_keys=[Situacao])
    interessado_related = relationship("Interessado", foreign_keys=[CgcCpf])
    segmento_related = relationship("Segmento", foreign_keys=[Segmento])
    area_related = relationship("Area", foreign_keys=[Area])
    mecanismo_related = relationship("Mecanismo", foreign_keys=[Mecanismo])


class PlanoDistribuicao(PlanoDistribuicaoBase, Base):
    idPlanoDistribuicao = Column(Integer, primary_key=True)
    QtdeProduzida = Column(Integer)
    QtdeProponente = Column(Integer)
    QtdePatrocinador = Column(Integer)
    QtdeOutros = Column(Integer)
    QtdeVendaNormal = Column(Integer)
    QtdeVendaPromocional = Column(Integer)
    QtdeUnitarioNormal = Column(Integer)
    QtdeUnitarioPromocional = Column(Integer)
    PrecoUnitarioPromocional = Column(Money)
    PrecoUnitarioNormal = Column(Money)
    stPlanoDistribuicaoProduto = Column(Boolean)
    stPrincipal = Column(Boolean)
    idProjeto = Column(Integer, ForeignKey(foreign_key(ProjetosBase, "idProjeto")))
    idProduto = Column(Integer, ForeignKey(foreign_key(ProdutoBase, "Codigo")))
    idPosicaoDaLogo = Column(Integer, ForeignKey(foreign_key(VerificacaoBase, "idVerificacao")))

    # Original table does not use a foreign key constraint
    Segmento = Column(String, ForeignKey(foreign_key(SegmentoBase, "Codigo")))
    Area = Column(CHAR, ForeignKey(foreign_key(AreaBase, "Codigo")))

    # Related fields
    area_related = relationship('Area', foreign_keys=[Area])
    produto_related = relationship('Produto', foreign_keys=[idProduto])
    projeto_related = relationship('Projeto', foreign_keys=[idProjeto])
    segmento_related = relationship('Segmento', foreign_keys=[Segmento])
    verificacao_related = relationship('Verificacao',
                                       foreign_keys=[idPosicaoDaLogo])


class PlanilhaAprovacao(PlanilhaAprovacaoBase, Base):  # noqa: N801
    idPlanilhaAprovacao = Column(Integer, primary_key=True)
    idPlanilhaItem = Column(Integer,
                            ForeignKey(foreign_key(PlanilhaItensBase, "idPlanilhaItens")))
    idPronac = Column(Integer, ForeignKey(foreign_key(ProjetosBase, "IdPRONAC")))
    idEtapa = Column(Integer, ForeignKey(foreign_key(PlanilhaEtapaBase, "idPlanilhaEtapa")))
    idUnidade = Column(Integer, ForeignKey(foreign_key(PlanilhaUnidadeBase, "idUnidade")))
    qtItem = Column(Integer)
    vlUnitario = Column(Integer)
    nrOcorrencia = Column(Integer)


class Deslocamento(DeslocamentoBase, Base):
    idDeslocamento = Column(Integer, primary_key=True)
    Qtde = Column(Integer)
    idProjeto = Column(Integer, ForeignKey(foreign_key(ProjetosBase, "idProjeto")))
    idPaisOrigem = Column(Integer, ForeignKey(foreign_key(PaisBase, "idPais")))
    idUFOrigem = Column(Integer, ForeignKey(foreign_key(UFBase, "iduf")))
    idMunicipioOrigem = Column(Integer,
                               ForeignKey(foreign_key(MunicipiosBase, "idMunicipioIBGE")))
    idPaisDestino = Column(Integer, ForeignKey(foreign_key(PaisBase, "idPais")))
    idUFDestino = Column(Integer, ForeignKey(foreign_key(UFBase, "iduf")))
    idMunicipioDestino = Column(Integer,
                                ForeignKey(foreign_key(MunicipiosBase, "idMunicipioIBGE")))


class Prorrogacao(ProrrogacaoBase, Base):
    idProrrogacao = Column(Integer, primary_key=True)
    Logon = Column(Integer)
    DtPedido = Column(DateTime)
    DtInicio = Column(DateTime)
    DtFinal = Column(DateTime)
    Observacao = Column(String)
    Atendimento = Column(String)
    idPronac = Column(Integer)

