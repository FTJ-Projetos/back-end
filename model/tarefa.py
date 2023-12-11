from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column("pk_tarefa", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    comentario = Column(String(200))
    data_conclusao = Column(DateTime)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o tarefa e o comentário.
    # Essa relação é implicita, não está salva na tabela 'tarefa',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    #comentarios = relationship("Comentario")

    def __init__(self, nome:str, comentario:str, data_conclusao:DateTime,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Tarefa

        Arguments:
            nome: nome da tarefa.
            comentario: comentario sobre a tarefa
            data_conclusao: data prevista de conclusao
            data_insercao: data de quando a tarefa foi inserido à base
        """
        self.nome = nome
        self.comentario = comentario
        self.data_conclusao = data_conclusao

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    
