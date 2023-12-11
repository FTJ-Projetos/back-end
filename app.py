from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from datetime import datetime


from sqlalchemy.exc import IntegrityError

from model import Session, Tarefa
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Tarefas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
#home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tarefa_tag = Tag(name="Tarefa", description="Adição, visualização e remoção de tarefas à base")





@app.post('/tarefa', tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})

        
def add_tarefa(form: TarefaSchema):
    """Adiciona uma nova Tarefa à base de dados

    Retorna uma representação dos tarefas e comentários associados.
    """
    tarefa = Tarefa(
        nome=form.nome,
        comentario=form.comentario,
        data_conclusao=form.data_conclusao)
    logger.debug(f"Adicionanda tarefa com nome: '{tarefa.nome}'")
    try:
        
        # criando conexão com a base
        session = Session()
        # adicionando tarefa
        session.add(tarefa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada tarefa com nome: '{tarefa.nome}'")
        return apresenta_tarefa(tarefa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Tarefa com mesmo nome já salva na base :/"
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova tarefa :/"
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/tarefas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas():
    """Faz a busca por todas as Tarefa cadastradas

    Retorna uma representação da listagem de tarefas.
    """
    logger.debug(f"Coletando tarefas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tarefas = session.query(Tarefa).all()

    if not tarefas:
        # se não há tarefas cadastrados
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tarefas))
        # retorna a representação de tarefa
        print(tarefas)
        return apresenta_tarefas(tarefas), 200



@app.delete('/tarefa', tags=[tarefa_tag],
            responses={"200": TarefaDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefaBuscaSchema):
    """Remove um Tarefa a partir do nome da tarefa informada

    Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_nome = unquote(unquote(query.nome))
    print(tarefa_nome)
    logger.debug(f"Removendo dados sobre a tarefa #{tarefa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Tarefa).filter(Tarefa.nome == tarefa_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada a tarefa #{tarefa_nome}")
        return {"mesage": "Tarefa removida", "id": tarefa_nome}
    else:
        # se o tarefa não foi encontrado
        error_msg = "Tarefa não encontrado na base :/"
        logger.warning(f"Erro ao deletar tarefa #'{tarefa_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


