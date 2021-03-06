from .query import PreProjetoQuery
from .pre_projeto_detail import PreProjetoDetail
from ..resource import ListResource


class PreProjetoList(ListResource):
    query_class = PreProjetoQuery
    resource_path = 'propostas'
    embedding_field = 'propostas'
    detail_resource_class = PreProjetoDetail
    detail_pk = 'id'
    sort_fields = {
        'nome',
        'id',
        'data_aceite',
        'data_arquivamento',
    }
    default_sort_field = 'id'
    non_filtering_args = {'data_inicio_min', 'data_inicio_max', 'data_termino_min', 'data_termino_max'}
    filter_likeable_fields = {
        'nome',
        'area'
        'situacao',  # TODO: This like can take a very long time to resolve
        'data_inicio',
        'data_termino'
    }
