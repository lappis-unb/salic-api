import graphene

from .queries import IncentivadorGQLQuery, DoacaoGQLQuery, \
    ProponenteGQLQuery, PropostaGQLQuery, FornecedorGQLQuery, \
    ProjetoGQLQuery, UFCountGQLQuery, AreaGQLQuery, DeslocamentosGQLQuery, \
    DistribuicaoGQLQuery

class RootQuery(IncentivadorGQLQuery, DoacaoGQLQuery, ProponenteGQLQuery,
                PropostaGQLQuery, FornecedorGQLQuery, ProjetoGQLQuery,
                UFCountGQLQuery, AreaGQLQuery, DeslocamentosGQLQuery,
                DistribuicaoGQLQuery):
    pass


schema = graphene.Schema(query=RootQuery, auto_camelcase=False)
