from .fornecedor_detail import FornecedorDetail
from .query import FornecedorQuery
from ..resource import ListResource
from ...utils import encrypt


class FornecedorList(ListResource):
    """
    Class related with informations about Fornecedores' list of one project
    """

    query_class = FornecedorQuery
    resource_path = 'fornecedores'
    embedding_field = 'fornecedores'
    detail_resource_class = FornecedorDetail
    detail_pk = 'cgccpf'
    default_sort_field = 'cgccpf'
    sort_fields = {
        'cgccpf', 'nome'
    }
    filter_likeable_fields = {
        'cgccpf', 'nome'
    }
    request_args = {
        'nome', 'fornecedor_id', 'cgccpf', 'PRONAC', 'limit', 'offset',
        'format', 'sort'
    }

    def prepared_detail_object(self, item):
        detail_resource = super().prepared_detail_object(item)
        detail_resource.args['fornecedor_id'] = encrypt(item['cgccpf'])
        return detail_resource
