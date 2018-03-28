from .query import AreaQuery
from ..resource import ListResource, DetailResource

class AreaDetail(DetailResource):
    def hal_links(self, result):
        """
        Responsable for generate link for Area filter for project
        """
        return {
            'self': self.url('/projetos/?area=%s' % result['codigo']),
        }

class Area(ListResource):
    resource_path = 'projetos/areas'
    detail_resource_class = AreaDetail
    query_class = AreaQuery
    embedding_field = 'areas'
    has_pagination = False
    request_args = set()
    sort_fields = {}
    detail_pk = 'codigo'

