from .query import FornecedorQuery
from ..resource import DetailResource
from ...utils import decrypt


class FornecedorDetail(DetailResource):
    """
    Class related with information about an specific Fornecedor
    """
    query_class = FornecedorQuery
    resource_path = 'fornecedores'
    csv_columns = ['email', 'nome', 'cgccpf']
    request_args = {'fornecedor_id', 'format'}

    def build_query_args(self):
        args = super().build_query_args()
        fornecedor_id = args.pop('fornecedor_id')
        args['cgccpf'] = decrypt(fornecedor_id)
        return args

    def hal_links(self, result):
        """
        Responsable for generate Fornecedores' urls
        """
        fornecedor_id = self.args['fornecedor_id']
        return {
            'self': self.url('/fornecedores/%s' % fornecedor_id),
            'produtos': self.url('/fornecedores/%s/produtos' % fornecedor_id),
        }
