from sqlalchemy import func

from ..query import Query
from ..projeto.query import ProjetoQuery
from ..projeto.projeto_list import ProjetoList

from ...models import Interessado, UF, Projeto, Captacao, Segmento, PreProjeto,Area, Situacao, Mecanismo, Enquadramento


class ContagemQuery(Query):
    labels_to_fields = ProjetoQuery.labels_to_fields
    fields_already_filtered = ProjetoQuery.fields_already_filtered
    transform_args = ProjetoList.transform_args
    filter_likeable_fields = ProjetoList.filter_likeable_fields
    sort_fields={}
    default_sort_field=None


class IncentivadorUFQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(func.count(Interessado.CgcCpf).label("quantidade"), Interessado.Uf.label("local"))
        query = (query
            .select_from(Captacao)
            .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
            .join(PreProjeto)
            .join(Area)
            .join(Segmento)
            .join(Situacao)
            .join(Mecanismo, Mecanismo.Codigo == Projeto.Mecanismo)
            .outerjoin(Enquadramento,
                Enquadramento.IdPRONAC == Projeto.IdPRONAC))
        query = query.group_by(Interessado.Uf)
        return query


class IncentivadorRegiaoQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(func.count(Interessado.CgcCpf).label("quantidade"), UF.Regiao.label("local"))
        query = (query
            .select_from(Captacao)
            .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
            .join(UF, UF.Sigla == Interessado.Uf)
            .join(PreProjeto)
            .join(Area)
            .join(Segmento)
            .join(Situacao)
            .join(Mecanismo, Mecanismo.Codigo == Projeto.Mecanismo)
            .outerjoin(Enquadramento,
                Enquadramento.IdPRONAC == Projeto.IdPRONAC))
        query = query.group_by(UF.Regiao)
        return query


class ProponenteRegiaoQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(func.count(Interessado.CgcCpf).label("quantidade"),
            UF.Regiao.label("local")
        )
        
        query = query.select_from(Interessado)
        query = (query
            .join(Projeto)
            .join(UF, UF.Sigla == Interessado.Uf)
            .join(PreProjeto)
            .join(Area)
            .join(Segmento)
            .join(Situacao)
            .join(Mecanismo, Mecanismo.Codigo == Projeto.Mecanismo)
            .outerjoin(Enquadramento,
                Enquadramento.IdPRONAC == Projeto.IdPRONAC))

        query = query.filter(Projeto.idProjeto.isnot(None))
        query = query.group_by(UF.Regiao)
        return query


class ProponenteUFQuery(ContagemQuery):
    def query(self, **kwargs):
        query = Query().raw_query(func.count(Interessado.CgcCpf).label("quantidade"),
         Interessado.Uf.label("local"))
        
        query = query.select_from(Interessado)
        query = (query
            .join(Projeto)
            .join(PreProjeto)
            .join(Area)
            .join(Segmento)
            .join(Situacao)
            .join(Mecanismo, Mecanismo.Codigo == Projeto.Mecanismo)
            .outerjoin(Enquadramento,
                Enquadramento.IdPRONAC == Projeto.IdPRONAC))

        query = query.filter(Projeto.idProjeto.isnot(None))
        query = query.group_by(Interessado.Uf)
        return query


        