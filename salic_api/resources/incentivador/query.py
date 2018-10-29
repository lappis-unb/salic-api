from sqlalchemy import func
from ..query import Query
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
        'PRONAC': Captacao.PRONAC,
    }

    @property
    def query_fields(self):
        black_list = {'PRONAC'}
        return tuple(v.label(k) for k, v in self.labels_to_fields.items() if k not in black_list)

    def query(self, limit=1, offset=0, **kwargs):
        query = self.raw_query(*self.query_fields).join(Captacao)
        if 'PRONAC' in kwargs:
            pronac = kwargs['PRONAC']
            year = pronac[:2]
            seq = pronac[2:]
            query = (
                query
                    .filter(Captacao.Sequencial == seq, Captacao.AnoProjeto == year)
            )
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

    def query(self, limit=100, offset=0, **kwargs):
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
