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

    def build_links(self, args={}):

        self.projetos_links = []

        for PRONAC in args['projetos_PRONAC']:
            link = current_app.config['API_ROOT_URL'] + 'projetos/%s/' % PRONAC
            self.projetos_links.append(link)

        self.incentivador_links = []

        for incentivador_id in args['incentivador_ids']:
            url_id = encrypt(incentivador_id)
            link = current_app.config['API_ROOT_URL'] + \
                'incentivadores/?url_id=%s' % url_id
            self.projetos_links.append(link)

    def hal_builder(self, data, args=None):
        captacoes = []

        for index in range(len(data['captacoes'])):

            captacao = data['captacoes'][index]

            projeto_link = self.projetos_links[index]
            incentivador_link = self.incentivador_links[index]

            captacao['_links'] = {}
            captacao['_links']['projeto'] = projeto_link
            captacao['_links']['incentivador'] = incentivador_link

        data['_embedded'] = {'captacoes': captacoes}
        del data['captacoes']

        return data
