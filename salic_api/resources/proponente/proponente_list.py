from .query import ProponenteQuery
from .proponente_detail import ProponenteDetail
from ..resource import ListResource
from ...utils import encrypt


class ProponenteList(ListResource):
    query_class = ProponenteQuery
    resource_path = 'proponentes'
    embedding_field = 'proponentes'
    detail_resource_class = ProponenteDetail
    detail_pk = 'cgccpf'
    default_sort_field = 'total_captado'

    sort_fields = {
        'total_captado', 'nome', 'cgccpf', 'municipio', 'UF',
        'tipo_pessoa'
    }

    filter_likeable_fields = {
        'nome', 'cgccpf'
    }

    request_args = {
        'nome', 'cgccpf', 'proponente_id', 'municipio', 'UF', 'tipo_pessoa',
        'limit', 'offset', 'format'
    }

    def prepared_detail_object(self, item):
        detail_resource = super().prepared_detail_object(item)
        detail_resource.args['proponente_id'] = encrypt(item['cgccpf'])
        return detail_resource
