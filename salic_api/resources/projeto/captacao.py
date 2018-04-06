import logging

from flask import current_app

from .query import CaptacaoQuery
from ..resource import ListResource
from ...utils import encrypt

class Captacao(ListResource):
    query_class = CaptacaoQuery
    embedding_field = 'captacoes'

    @property
    def resource_path(self):
        return "%s/%s/%s" % ("projetos", self.args['PRONAC'], 'captacoes')
