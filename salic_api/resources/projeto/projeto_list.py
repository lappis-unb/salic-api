from .query import ProjetoQuery
from .projeto_detail import ProjetoDetail
from ..resource import ListResource


class ProjetoList(ListResource):
    query_class = ProjetoQuery
    resource_path = 'projetos'
    embedding_field = 'projetos'
    detail_resource_class = ProjetoDetail
    detail_pk = 'PRONAC'

    sort_fields = {
        'ano_projeto', 'PRONAC',
        'valor_solicitado', 'outras_fontes', 'valor_captado', 'valor_proposta',
        'valor_aprovado', 'valor_projeto',
    }
    default_sort_field = 'ano_projeto'
    non_filtering_args = {'data_inicio_min', 'data_inicio_max', 'data_termino_min', 'data_termino_max'}
    filter_likeable_fields = {
        'proponente',
        'cgccpf',
        'nome',
        'area',
        'situacao',  # TODO: This like can take a very long time to resolve,
        'data_inicio',
        'data_termino'
    }
