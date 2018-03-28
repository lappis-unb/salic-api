from .query import AreaQuery
from ..resource import ListResource


class Area(ListResource):
    resource_path = 'projetos/areas'
    query_class = AreaQuery
    embedding_field = 'areas'
    has_pagination = False
    request_args = set()
    sort_fields = {}

    def hal_item_links(self, item):
        link = self.url('/projetos/?area=%s' % item['codigo'])
        return {'self': link}
