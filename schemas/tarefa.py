from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from model.tarefa import Tarefa


class TarefaSchema(BaseModel):
    """ Define como um novo tarefa a ser inserido deve ser representado
    """
    nome: str = "Entregar MVP"
    comentario: str = "Teste"
    data_conclusao: date = "2023-12-11"


class TarefaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do tarefa.
    """
    nome: str = "Teste"


class ListagemTarefasSchema(BaseModel):
    """ Define como uma listagem de tarefas será retornada.
    """
    tarefas:List[TarefaSchema]


def apresenta_tarefas(tarefas: List[Tarefa]):
    """ Retorna uma representação do tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    result = []
    for tarefa in tarefas:
        result.append({
            "nome": tarefa.nome,
            "comentario": tarefa.comentario,
            "data_conclusao": tarefa.data_conclusao
        })

    return {"tarefas": result}


class TarefaViewSchema(BaseModel):
    """ Define como um tarefa será retornado: tarefa + comentários.
    """
    id: int = 1
    nome: str = "Trabalho"
    comentario: str = "Teste"
    data_conclusao: date = "2023-01-01"
   

class TarefaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_tarefa(tarefa: Tarefa):
    """ Retorna uma representação do tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    return {
        "id": tarefa.id,
        "nome": tarefa.nome,
        "comentario": tarefa.comentario,
        "data_conclusao": tarefa.data_conclusao
    }
