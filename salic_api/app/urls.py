import os

from flask import redirect, send_from_directory
from flask_cors import CORS
from flask_restful import Api
from flask_graphql import GraphQLView

from ..resources.fornecedor.fornecedor_detail import FornecedorDetail
from ..resources.fornecedor.fornecedor_list import FornecedorList
from ..resources.fornecedor.produto import Produto
from ..resources.incentivador.doacao import DoacaoList
from ..resources.incentivador.incentivador_detail import IncentivadorDetail
from ..resources.incentivador.incentivador_list import IncentivadorList
from ..resources.preprojeto.pre_projeto_detail import PreProjetoDetail
from ..resources.preprojeto.pre_projeto_list import PreProjetoList
from ..resources.projeto.area import Area
from ..resources.projeto.captacao import Captacao
from ..resources.projeto.projeto_detail import ProjetoDetail
from ..resources.projeto.projeto_list import ProjetoList
from ..resources.projeto.segmento import Segmento
from ..resources.proponente.proponente_detail import ProponenteDetail
from ..resources.proponente.proponente_list import ProponenteList
from ..resources.test_resource import TestResource
from ..salic_graphql.schema import schema

dirname = os.path.dirname
BASE_PATH = dirname(dirname(__file__))
STATIC_URL_PATH = os.path.join(BASE_PATH, 'static')
SWAGGER_DEF = 'swagger_specification_PT-BR.json'



def make_urls(app=None):
    if app is None:
        from flask import current_app as app

    api = Api(app)
    api.add_resource(TestResource, '/test', '/test/')

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Register resources to urls
    base_version = app.config['BASE_VERSION']

    def register(resource, url):
        url = url.strip('/')
        api.add_resource(resource, '/%s/%s' % (base_version, url),
                         '/%s/%s/' % (base_version, url))

    register(ProjetoDetail, 'projetos/<string:PRONAC>/')
    register(ProjetoList, 'projetos/')
    register(ProponenteList, 'proponentes/')
    register(ProponenteDetail, 'proponentes/<string:proponente_id>/')
    register(Captacao, 'projetos/<string:PRONAC>/captacoes/')
    register(Area, 'projetos/areas')
    register(Segmento, 'projetos/segmentos/')
    register(PreProjetoList, 'propostas/')
    register(PreProjetoDetail, 'propostas/<string:id>/')
    register(IncentivadorList, 'incentivadores/')
    register(IncentivadorDetail, 'incentivadores/<string:incentivador_id>/')
    register(DoacaoList, 'incentivadores/<string:incentivador_id>/doacoes/')
    register(FornecedorList, 'fornecedores/')
    register(FornecedorDetail, 'fornecedores/<string:fornecedor_id>/')
    register(Produto, 'fornecedores/<string:fornecedor_id>/produtos/')

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
        ))

    app.add_url_rule(
        '/graphiql',
        view_func=GraphQLView.as_view(
            'graphiql',
            schema=schema,
            graphiql=True
        ))

    @app.route('/')
    def index():
        return redirect("/doc/", code=302)

    @app.route('/v1/swagger-def/')
    def swagger_def():
        return send_from_directory(BASE_PATH, SWAGGER_DEF)

    @app.route('/doc/')
    def documentation():
        return send_from_directory(STATIC_URL_PATH, 'index.html')

    @app.route('/doc/<path:path>')
    def documentation_data(path):
        return send_from_directory(STATIC_URL_PATH, path)
