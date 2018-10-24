from ..query import Query
from ...models import PreProjeto, Mecanismo, Projeto, Area, Situacao


class PreProjetoQuery(Query):

    labels_to_fields = {
        'nome': PreProjeto.NomeProjeto,
        'id': PreProjeto.idPreProjeto,
        'data_inicio': PreProjeto.data_inicio_execucao,
        'data_inicio_min': PreProjeto.data_inicio_execucao,
        'data_inicio_max': PreProjeto.data_inicio_execucao,
        'data_termino': PreProjeto.data_final_execucao,
        'data_termino_min': PreProjeto.data_final_execucao,
        'data_termino_max': PreProjeto.data_final_execucao,
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
        'situacao': Situacao.Descricao,
    }

    @property
    def query_fields(self):
        black_list = {'data_inicio_min', 'data_inicio_max', 'data_termino_min', 'data_termino_max'}
        return tuple(v.label(k) for k, v in self.labels_to_fields.items() if k not in black_list)

    def query(self, limit=1, offset=0, data_inicio=None, data_inicio_min=None,
            data_inicio_max=None, data_termino=None, data_termino_min=None,
            data_termino_max=None, **kwargs):
        query = self.raw_query(*self.query_fields)
        query = query.select_from(PreProjeto)
        query = query.join(Mecanismo)
        query = query.join(Projeto, PreProjeto.idPreProjeto == Projeto.idProjeto)

        # # Filter query by dates
        end_of_day = (lambda x: None if x is None else x + ' 23:59:59')
        if data_inicio_min is not None:
            query = query.filter(PreProjeto.data_inicio_execucao >= data_inicio_min)

        if data_inicio_max is not None:
            query = query.filter(PreProjeto.data_inicio_execucao <= end_of_day(data_inicio_max))

        if data_termino_min is not None:
            query = query.filter(PreProjeto.data_final_execucao >= data_termino_min)

        if data_termino_max is not None:
            query = query.filter(PreProjeto.data_final_execucao <= end_of_day(data_termino_max))

        return query
