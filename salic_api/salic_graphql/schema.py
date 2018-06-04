import graphene

from .queries import IncentivadorGQLQuery, DoacaoGQLQuery, \
    ProponenteGQLQuery, PropostaGQLQuery, FornecedorGQLQuery, \
    ProjetoGQLQuery, UFCountGQLQuery

class RootQuery(IncentivadorGQLQuery, DoacaoGQLQuery, ProponenteGQLQuery,
                PropostaGQLQuery, FornecedorGQLQuery, ProjetoGQLQuery, UFCountGQLQuery):
    pass


schema = graphene.Schema(query=RootQuery, auto_camelcase=False)
