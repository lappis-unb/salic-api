from os import environ as env
from sqlalchemy import func

from ..projeto.query import custo_projeto
from ..query import Query, filter_query, filter_query_like
from ...models import Interessado, Projeto, Custos

use_sql_procedures = False if env.get('SQL_DRIVER', 'sqlite') == 'sqlite' else True


class ProponenteQuery(Query):

    if not use_sql_procedures:
        labels_to_fields = {
            'total_captado': custo_projeto,
            'nome': Interessado.Nome,
            'municipio': Interessado.Cidade,
            'UF': Interessado.Uf,
            'responsavel': Interessado.Responsavel,
            'cgccpf': Interessado.CgcCpf,
            'tipo_pessoa': Interessado.tipoPessoaLabel,
        }
    else:
        labels_to_fields = {
            'total_captado': func.sum(func.sac.dbo.fnCustoProjeto (Projeto.AnoProjeto, Projeto.Sequencial)),
            'nome': Interessado.Nome,
            'municipio': Interessado.Cidade,
            'UF': Interessado.Uf,
            'responsavel': Interessado.Responsavel,
            'cgccpf': Interessado.CgcCpf,
            'tipo_pessoa': Interessado.tipoPessoaLabel,
        }

    group_by_fields = (
        Interessado.Nome,
        Interessado.Cidade,
        Interessado.Uf,
        Interessado.Responsavel,
        Interessado.CgcCpf,
        Interessado.tipoPessoa,
    )

    def query(self, limit=1, offset=0, nome=None, cgccpf=None, municipio=None,
              UF=None, tipo_pessoa=None):

        query = self.raw_query(*self.query_fields)
        query = query.select_from(Interessado)

        if not use_sql_procedures:
            query = query.join(Custos)

        query = query.group_by(*self.group_by_fields)
        query = query.filter(Projeto.idProjeto.isnot(None))

        return query

    def sorted(self, query, sort_field, sort_order):
        # start_row = offset
        # end_row = offset + limit

        sort_mapping_fields = {
            'cgccpf': Interessado.CgcCpf,
            'total_captado': func.sum(
                func.sac.dbo.fnCustoProjeto(Projeto.AnoProjeto,
                                            Projeto.Sequencial))
        }

        if sort_field is None:
            sort_field = 'cgccpf'

        sort_field = sort_mapping_fields[sort_field]

        return query
####################################


#         # order by descending
#         if sort_order == 'desc':
#             query = query.order_by(desc(sort_field))
#         # order by ascending
#         else:
#             query = query.order_by(sort_field)
#
#         total_records = query.count()
#
#         query = query.slice(start_row, end_row)
#
#         return res.query(), total_records
