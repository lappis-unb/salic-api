from sqlalchemy import Column, Integer, String

from .base import Base, UsuariosBase


class Usuarios(UsuariosBase, Base):
    """
    Tabela que armazena dados do usuário.
    """
    usu_codigo = Column(Integer, primary_key=True)
    usu_nome = Column(String)
