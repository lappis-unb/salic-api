from .query import CaptacaoQuery
from ..resource import ListResource


class Captacao(ListResource):
    query_class = CaptacaoQuery
    embedding_field = 'captacoes'

    @property
    def resource_path(self):
        return "%s/%s/%s" % ("projetos", self.args['PRONAC'], 'captacoes')
