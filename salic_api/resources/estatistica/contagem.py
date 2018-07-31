from sqlalchemy import func

from ..query import Query
from ..projeto.query import ProjetoQuery
from ..projeto.projeto_list import ProjetoList

from ...models import Interessado, UF, Projeto, Captacao, Segmento, \
    PreProjeto, Area, Situacao, Mecanismo, Enquadramento


def join_projeto_fields(query):
        query = (
            query
            .join(Area)
            .join(Segmento)
            .join(Situacao)
            .join(Mecanismo, Mecanismo.Codigo == Projeto.Mecanismo)
            .outerjoin(Enquadramento,
                       Enquadramento.IdPRONAC == Projeto.IdPRONAC)
        )

        return query


class ContagemQuery(Query):
    labels_to_fields = ProjetoQuery.labels_to_fields
    fields_already_filtered = ProjetoQuery.fields_already_filtered
    transform_args = ProjetoList.transform_args
    filter_likeable_fields = ProjetoList.filter_likeable_fields
    sort_fields = {}
    default_sort_field = None


class IncentivadorUFQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Interessado.CgcCpf.distinct()).label("quantidade"),
            Interessado.Uf.label("local"))
        query = (
            query
            .select_from(Interessado)
            .join(Captacao, Captacao.CgcCpfMecena == Interessado.CgcCpf)
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC))
        query = join_projeto_fields(query)
        query = query.group_by(Interessado.Uf)
        return query


class IncentivadorRegiaoQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Interessado.CgcCpf.distinct()).label("quantidade"),
            UF.Regiao.label("local"))
        query = (
            query
            .select_from(Captacao)
            .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
            .join(UF, UF.Sigla == Interessado.Uf))
        query = join_projeto_fields(query)
        query = query.group_by(UF.Regiao)
        return query


class ProponenteRegiaoQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Interessado.CgcCpf.distinct()).label("quantidade"),
            UF.Regiao.label("local")
        )

        query = query.select_from(Interessado)
        query = (
            query
            .join(Projeto)
            .join(UF, UF.Sigla == Interessado.Uf)
            .join(PreProjeto))
        query = join_projeto_fields(query)
        query = query.filter(Projeto.idProjeto.isnot(None))
        query = query.group_by(UF.Regiao)
        return query


class ProponenteUFQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Interessado.CgcCpf.distinct()).label("quantidade"),
            Interessado.Uf.label("local"))

        query = query.select_from(Interessado)
        query = (
            query
            .join(Projeto)
            .join(PreProjeto))
        query = join_projeto_fields(query)
        query = query.filter(Projeto.idProjeto.isnot(None))
        query = query.group_by(Interessado.Uf)
        return query


class ProjetoUFQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Projeto.PRONAC.distinct()).label("quantidade"),
            Projeto.UfProjeto.label("local"))
        query = query.select_from(Projeto)
        query = (
            query
            .join(PreProjeto)
            .join(Interessado))
        query = join_projeto_fields(query)
        query = query.group_by(Projeto.UfProjeto)
        return query


class ProjetoRegiaoQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Projeto.PRONAC.distinct()).label("quantidade"),
            UF.Regiao.label("local")
        )

        query = query.select_from(Projeto)
        query = (
            query
            .join(UF, UF.Sigla == Projeto.UfProjeto)
            .join(PreProjeto)
            .join(Interessado))
        query = join_projeto_fields(query)
        query = query.group_by(UF.Regiao)
        return query


class SegmentoCountQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Projeto.PRONAC.distinct()).label("quantidade"),
            Segmento.Descricao.label("segmento"))

        query = query.select_from(Projeto)
        query = (
            query
            .join(PreProjeto)
            .join(Interessado))
        query = join_projeto_fields(query)
        query = query.group_by(Segmento.Descricao)
        return query


class AreaCountQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(
            func.count(Projeto.PRONAC.distinct()).label("quantidade"),
            Area.Descricao.label("area"))

        query = query.select_from(Projeto)
        query = (
            query
            .join(PreProjeto)
            .join(Interessado))
        query = join_projeto_fields(query)
        query = query.group_by(Area.Descricao)
        return query
