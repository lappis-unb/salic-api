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
        'data_inicio',
        'data_termino',
        'data_aceite',
        'data_arquivamento',
    }
    default_sort_field = 'id'
    filter_likeable_fields = {'nome'}
