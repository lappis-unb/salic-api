from datetime import datetime

from ..models import Area, Arquivo, Projeto, PreProjeto, Segmento, \
    Enquadramento, Mecanismo, Situacao, Interessado, Captacao, \
    CertidoesNegativas, Verificacao, PlanoDivulgacao, Produto, \
    PlanoDistribuicao, PlanilhaAprovacao, PlanilhaItens, PlanilhaEtapa, \
    PlanilhaUnidade, Readequacao, TipoReadequacao, TipoEncaminhamento

#
# Global constants
#
CPF = '1234'


def areas_example():
    return [
        Area(Codigo='1', Descricao='Artes Cênicas'),
        Area(Codigo='2', Descricao='Audiovisual'),
        Area(Codigo='3', Descricao='Música'),
    ]


def projeto_example(size=1):
    return [Projeto(IdPRONAC=20001234, AnoProjeto='2000', Sequencial='1234',
                    NomeProjeto='Test', Localizacao='Brazil',
                    DtInicioExecucao=datetime(2000, 1, 1),
                    DtFimExecucao=datetime(2000, 2, 1),
                    UfProjeto='DF', SolicitadoReal='R$%s.000.000' % i,
                    SolicitadoUfir='R$%s.000.000' % i,
                    SolicitadoCusteioUfir='R$%s.000.000' % i,
                    SolicitadoCusteioReal='R$%s.000.000' % i,
                    SolicitadoCapitalUfir='R$%s.000.000' % i,
                    SolicitadoCapitalReal='R$%s.000.000' % i,
                    ResumoProjeto='abstract', ProvidenciaTomada='nenhuma',
                    Segmento='11', Situacao='%s' % i,
                    Area='%s' % i, CgcCpf=CPF, idProjeto=i, Mecanismo='%s' % i)
            for i in range(1, size + 1)]


def pre_projeto_example(size=1):
    return [PreProjeto(idPreProjeto=i, NomeProjeto='NomeProjeto %s' % i,
                       DtInicioDeExecucao=datetime(2000, 1, 1),
                       DtFinalDeExecucao=datetime(2000, 2, 1),
                       dtAceite=datetime(2000, 1, 1),
                       DtArquivamento=datetime(2000, 3, 1),
                       Mecanismo=i % 2 + 1, Objetivos='cultural',
                       Justificativa='Justificativa %s' % i,
                       Acessibilidade='Acessibilidade',
                       DemocratizacaoDeAcesso='DemocratizacaoDeAcesso',
                       EtapaDeTrabalho='EtapaDeTrabalho',
                       FichaTecnica='FichaTecnica',
                       ResumoDoProjeto='ResumoDoProjeto %s' % i,
                       Sinopse='Sinopse %s' % i,
                       ImpactoAmbiental='ImpactoAmbiental %s' % i,
                       EspecificacaoTecnica='EspecificacaoTecnica %s' % i,
                       EstrategiadeExecucao='EstrategiadeExecucao %s' % i)
            for i in range(1, 1 + size)]


def segmento_example():
    return [
        Segmento(Codigo='11', Descricao='Teatro', tpEnquadramento='2'),
        Segmento(Codigo='21', Descricao='Jogos Eletrônicos',
                 tpEnquadramento='1'),
    ]


def enquadramento_example(size=1):
    return [Enquadramento(Enquadramento=i, AnoProjeto='2000',
                          Sequencial='1234', IdPRONAC=20001234)
            for i in range(1, size + 1)]


def mecanismo_example():
    return [
        Mecanismo(Codigo='1', Descricao='Mecenato'),
        Mecanismo(Codigo='2', Descricao='FNC'),
    ]


def situacao_example(size=1):
    return [Situacao(Codigo='%s' % i, Descricao='Descricao %s' % i)
            for i in range(1, size + 1)]


def interessado_example(size=1):
    # tipoPessoa 2 e pessoa juridica
    return [Interessado(CgcCpf=CPF, Nome='Nome %s' % i,
                        Responsavel='Responsavel %s' % i, Uf='UF %s' % i,
                        Cidade='Cidade %s' % i, tipoPessoa='2')
            for i in range(1, size + 1)]


def captacao_example():
    return [Captacao(
        AnoProjeto='2000',
        Sequencial='1234',
        CaptacaoReal='CaptacaoReal',
        DtRecibo=datetime(2000, 1, 1),
        CgcCpfMecena=CPF,
    )]


def certidoes_negativas_example(size=1):
    return [CertidoesNegativas(AnoProjeto='2000', Sequencial='1234',
                               DtEmissao=datetime(2000, 1, 1),
                               DtValidade=datetime(2000, 3, 1),
                               CodigoCertidao=i, cdSituacaoCertidao=i,
                               CgcCpf=CPF)
            for i in range(1, size + 1)]


def verificacao_example(size=1):
    return [Verificacao(idTipo=i, Descricao='Descricao %s' % i, stEstado=True)
            for i in range(1, size + 1)]


def plano_divulgacao_example(size=1):
    return [PlanoDivulgacao(idPeca=i, idVeiculo=i, stPlanoDivulgacao=True,
                            idProjeto=i)
            for i in range(1, size + 1)]


def produto_example(size=1):
    return [Produto(Descricao='Produto %s' % i, Area='Area %s' % i,
                    Sintese='Sintese %s' % i, Idorgao=i, stEstado=True)
            for i in range(1, size + 1)]


def plano_distribuicao_example(size=1):
    return [PlanoDistribuicao(idPlanoDistribuicao=i, idProjeto=i, idProduto=i,
                              stPrincipal=True, Segmento='11', Area='%s' % i,
                              idPosicaoDaLogo=i,
                              PrecoUnitarioNormal='R$%s00' % i,
                              PrecoUnitarioPromocional='R$%s0' % i,
                              QtdeProduzida=0, QtdeProponente=0,
                              QtdePatrocinador=0, QtdeOutros=0,
                              QtdeVendaNormal=0, QtdeVendaPromocional=0,
                              QtdeUnitarioNormal=0, QtdeUnitarioPromocional=0,
                              stPlanoDistribuicaoProduto=False)
            for i in range(1, size + 1)]


def tbarquivo_example(size=1):
    return [Arquivo(idArquivo=i, nmArquivo='%s' % i)
            for i in range(1, size + 1)]


def tbplanilhaaprovacao_example(size=1):
    return [PlanilhaAprovacao(idPlanilhaAprovacao=i, idPlanilhaItem=i,
                              qtItem=i * 99, vlUnitario=3.1415, idEtapa=i,
                              idUnidade=i, idPronac=20001234, nrOcorrencia=15)
            for i in range(1, size + 1)]


def tbPlanilhaItens_example(size=1):
    return [PlanilhaItens(idPlanilhaItens=i, Descricao='Figurino %s' % i)
            for i in range(1, size + 1)]


def tbPlanilhaEtapa_example(size=1):
    return [PlanilhaEtapa(idPlanilhaEtapa=i, Descricao='Planilha Etapa %s' % i)
            for i in range(1, size + 1)]


def tbPlanilhaUnidade_example(size=1):
    return [PlanilhaUnidade(idUnidade=i, Descricao='Planilha Unidade %s' % i)
            for i in range(1, size + 1)]


def readequacao_example(size=1):
    return [Readequacao(idReadequacao=i, IdPRONAC=20001234,
                        dtSolicitacao=datetime(2000, 1, 1),
                        dsJustificativa="Descricao Justificativa %s" % i,
                        idSolicitante=i, idAvaliador=i,
                        dtAvaliador=datetime(2000, 1, 1),
                        dsAvaliacao="Descricao Avaliacao %s" % i,
                        idTipoReadequacao=i,
                        dsReadequacao="Descricao Readequacao %s" % i,
                        stAtendimento="Atendido",
                        siEncaminhamento=i,
                        dsEncaminhamento="Descricao Encaminhamento %s" % i,
                        dsSolicitacao='Solicitacao %s' % i,
                        stEstado='Estado %s' % i, idDocumento=i)
            for i in range(1, size + 1)]


def tipo_readequacao_example(size=1):
    return [TipoReadequacao(idTipoReadequacao=i,
                            dsReadequacao='Readequacao %s' % i)
            for i in range(1, size + 1)]


def tipo_encaminhamento_example(size=1):
    return [TipoEncaminhamento(idTipoEncaminhamento=i,
                               dsEncaminhamento='Encaminhamento %s' % i)
            for i in range(1, size + 1)]
