import graphene

from .queries import IncentivadorGQLQuery, DoacaoGQLQuery, \
    ProponenteGQLQuery, PropostaGQLQuery, FornecedorGQLQuery, \
    ProjetoGQLQuery


class RootQuery(IncentivadorGQLQuery, DoacaoGQLQuery, ProponenteGQLQuery,
                PropostaGQLQuery, FornecedorGQLQuery, ProjetoGQLQuery):
    pass


schema = graphene.Schema(query=RootQuery, auto_camelcase=False)
