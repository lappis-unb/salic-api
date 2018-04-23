from .query import DoacaoQuery
from ..format_utils import cgccpf_mask
from ..resource import ListResource, DetailResource
from ...utils import decrypt


class DoacaoDetail(DetailResource):
    def hal_links(self, result):
        encrypted_id = self.args['incentivador_id']
        incentivador_url = self.url('/incentivadores/%s' % encrypted_id)
        projeto_url = self.url('/projetos/%s' % result['PRONAC'])
        return {
            'projeto': projeto_url,
            'incentivador': incentivador_url,
        }

    def prepare_result(self, result):
        result["cgccpf"] = cgccpf_mask(result["cgccpf"])


class DoacaoList(ListResource):
    query_class = DoacaoQuery
    embedding_field = 'doacoes'
    detail_resource_class = DoacaoDetail
    detail_pk = 'cgccpf'
    request_args = {'incentivador_id', 'limit', 'offset', 'format'}
    sort_fields = {'data_recibo', 'valor', 'nome_projeto', 'cgccpf', 'nome_doador', 'PRONAC'}
    default_sort_field = 'valor'
    filter_likeable_fields = {'nome_doador'}

    def build_query_args(self):
        args = super().build_query_args()
        incentivador_id = args.pop('incentivador_id')
        args['cgccpf'] = decrypt(incentivador_id)
        return args

    @property
    def resource_path(self):
        return "%s/%s/%s" % (
            "incentivadores", self.args['incentivador_id'], 'doacoes')
