from sqlalchemy import Column, Integer, ForeignKey, String

from .base import *


# This table actually describes city names!
class Nomes(NomesBase, Base):
    idNome = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey(foreign_key(AgentesBase,'idAgente')))
    Descricao = Column(String)


class Agentes(AgentesBase, Base):
    idAgente = Column(Integer, primary_key=True)
    CNPJCPF = Column(String)


class Internet(InternetBase, Base):
    idInternet = Column(Integer, primary_key=True)
    idAgente = Column(Integer, ForeignKey(foreign_key(AgentesBase,'idAgente')))
    Descricao = Column(String)


class Pais(PaisBase, Base):
    idPais = Column(Integer, primary_key=True)
    Descricao = Column(String)


class UF(UFBase, Base):
    iduf = Column(Integer, primary_key=True)
    Descricao = Column(String)
    Sigla = Column(String)


class Municipios(MunicipiosBase, Base):
    idMunicipioIBGE = Column(Integer, primary_key=True)
    Descricao = Column(String)
