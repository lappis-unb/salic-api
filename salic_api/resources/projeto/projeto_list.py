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
        'ano_projeto', 'PRONAC', 'data_inicio', 'data_termino',
        'valor_solicitado', 'outras_fontes', 'valor_captado', 'valor_proposta',
        'valor_aprovado', 'valor_projeto',
    }
    default_sort_field = 'ano_projeto'
    filter_likeable_fields = {
        'proponente',
        'cgccpf',
        'nome',
    }
