from sqlalchemy import func
from sqlalchemy.sql.expression import desc

from ..query import Query, filter_query_like, filter_query
from ...models import Interessado, Projeto, Captacao
from ...utils import pc_quote


class IncentivadorQuery(Query):

    group_by_fields = (
        Interessado.Nome,
        Interessado.Cidade,
        Interessado.Uf,
        Interessado.Responsavel,
        Interessado.CgcCpf,
        Interessado.tipoPessoa,
    )

    labels_to_fields = {
        'nome': Interessado.Nome,
        'municipio': Interessado.Cidade,
        'UF': Interessado.Uf,
        'responsavel': Interessado.Responsavel,
        'cgccpf': Interessado.CgcCpf,
        'total_doado': func.sum(Captacao.CaptacaoReal),
        'tipo_pessoa': Interessado.tipoPessoaLabel,
    }

    def query(self, limit=1, offset=0, **kwargs):
        query = self.raw_query(*self.query_fields).join(Captacao)

        if 'PRONAC' in kwargs:
            query = query \
                .join(Projeto, Captacao.PRONAC == Projeto.PRONAC) \
                .filter(Captacao.PRONAC == kwargs['PRONAC'])

        return query.group_by(*self.group_by_fields)


class DoacaoQuery(Query):

    labels_to_fields = {
        'PRONAC': Captacao.PRONAC,
        'valor': Captacao.CaptacaoReal,
        'data_recibo': Captacao.data_recibo,
        'nome_projeto': Projeto.NomeProjeto,
        'cgccpf': Captacao.CgcCpfMecena,
        'nome_doador': Interessado.Nome,
    }

    def query(self, cgccpf, limit=100, offset=0, **kwargs):
        query = (
            self.raw_query(*self.query_fields)
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
            .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
        )

        return query

    def total(self, cgccpf):
        total = func.sum(Captacao.CaptacaoReal).label('total_doado')
        return (
            self.raw_query(total)
                .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
                .filter(Interessado.CgcCpf.like(pc_quote(cgccpf)))
        )
