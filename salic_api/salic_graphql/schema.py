import graphene

from .queries import IncentivadorGQLQuery, DoacaoGQLQuery, \
    ProponenteGQLQuery, PropostaGQLQuery, FornecedorGQLQuery, \
    ProjetoGQLQuery, UFCountGQLQuery, AreaGQLQuery

class RootQuery(IncentivadorGQLQuery, DoacaoGQLQuery, ProponenteGQLQuery,
                PropostaGQLQuery, FornecedorGQLQuery, ProjetoGQLQuery,
                UFCountGQLQuery, AreaGQLQuery):
    pass


schema = graphene.Schema(query=RootQuery, auto_camelcase=False)
