"""
Este módulo contém todos os modelos e tabelas do banco do SALIC no modelo do
ORM do SQL Alchemy. Apresentamos as tabelas organizadas pelo banco em que
aparecem no SALIC.
"""

from .agentes import Nomes, Agentes, Pais, Municipios, UF, Internet
from .bdcorporativo import Arquivo, ArquivoImagem, ComprovantePagamento, \
    ComprovantePagamentoxPlanilhaAprovacao, Documento, DocumentoProjeto, \
    ItemCusto
from .fake import Custos
from .sac import Projeto, PreProjeto, Area, Segmento, Enquadramento, Mecanismo, \
    Situacao, Interessado, Captacao, CertidoesNegativas, Verificacao, \
    PlanoDistribuicao, PlanoDivulgacao, Produto, Deslocamento, \
    PlanilhaAprovacao, PlanilhaEtapa, PlanilhaItens, PlanilhaUnidade, \
    Readequacao, TipoReadequacao, TipoEncaminhamento, Prorrogacao
from .tabelas import Usuarios
