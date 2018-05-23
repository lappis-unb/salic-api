from ..query import Query
from ...models import PreProjeto, Mecanismo, Projeto, Area


class PreProjetoQuery(Query):

    labels_to_fields = {
        'nome': PreProjeto.NomeProjeto,
        'id': PreProjeto.idPreProjeto,
        'data_inicio': PreProjeto.data_inicio_execucao,
        'data_termino': PreProjeto.data_final_execucao,
        'data_aceite': PreProjeto.data_aceite,
        'data_arquivamento': PreProjeto.data_arquivamento,
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
        'mecanismo': Mecanismo.Descricao,

        'UF': Projeto.UfProjeto,
        'PRONAC': Projeto.PRONAC,
        'area': Area.Descricao,
    }

    def query(self, limit=1, offset=0, **kwargs):
        query = self.raw_query(*self.query_fields)
        query = query.select_from(PreProjeto)
        query = query.join(Mecanismo)
        query = query.join(Projeto, PreProjeto.idPreProjeto == Projeto.idProjeto)

        return query
