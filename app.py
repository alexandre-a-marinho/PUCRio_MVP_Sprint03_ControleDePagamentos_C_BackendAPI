from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_caching import Cache
from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from model import Session, Pagamento
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Controle de Pagamentos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Seta cache
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pagamento_tag = Tag(name="Pagamento", description="Adição, visualização e remoção de pagamentos da base")
analise_tag = Tag(name="Análise", description="Estatísticas a análises sobre os pagamentos da base")


#  --------------------------------------------------------------------------------------
#  Rotas
#  --------------------------------------------------------------------------------------
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, permitindo escolher o estilo de documentação."""
    return redirect('/openapi')


@app.post('/pagamento', tags=[pagamento_tag],
          responses={"200": PagamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pagamento(form: PagamentoSchema):
    """Adiciona um novo Pagamento à base de dados.

    Retorna uma representação do Pagamento adicionado.
    """
    pagamento = Pagamento(
        descricao = form.descricao,
        categoria = form.categoria,
        subcategoria = form.subcategoria,
        valor = form.valor,
        num_parcelas = form.num_parcelas,
        data_insercao = date.today())
    # TODO: [1] Feature: allow user to add custom date
    
    logger.debug(f"Adicionando Pagamento descrito por: '{pagamento.descricao}'")
    try:
        # Cria conexão com a base
        session = Session()

        # Adiciona novo item na tabela e efetiva a adição (commit)
        session.add(pagamento)
        session.commit()
        logger.debug(f"Adicionado Pagamento descrito por: '{pagamento.descricao}'")
        valor_a_acrescentar = form.valor
        atualiza_cache_da_soma_pagamentos(valor_a_acrescentar)
        return apresenta_pagamento(pagamento), 200

    except IntegrityError as e:
        error_msg = "Erro de integridade na adição do novo Pagamento :/"
        logger.warning(f"Erro ao adicionar Pagamento #{pagamento.id}({pagamento.descricao}): {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso ocorra um erro fora do previsto
        error_msg = "Não foi possível salvar o novo Pagamento :/"
        logger.warning(f"Erro ao adicionar Pagamento #{pagamento.id}({pagamento.descricao}): {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/pagamentos', tags=[pagamento_tag],
         responses={"200": ListagemPagamentosSchema, "404": ErrorSchema})
def get_pagamentos():
    """Faz a busca por todos os Pagamentos cadastrados.

    Retorna uma representação da lista de todos os Pagamentos cadastrados (se
    existir algum).
    """
    logger.debug(f"Coletando Pagamentos ")
    
    # Cria conexão com a base para fazer a busca
    session = Session()
    pagamentos = session.query(Pagamento).all()

    if pagamentos:
        logger.debug(f"%d Pagamentos econtrados" % len(pagamentos))
        print(pagamentos)
        atualiza_cache_da_soma_pagamentos(0)
        # retorna a representação da lista dos Pagamentos encontrados
        return apresenta_pagamentos(pagamentos), 200
    else:
        # retorno vazio se nada for encontrado
        return {"pagamentos": []}, 200


@app.get('/pagamento', tags=[pagamento_tag],
         responses={"200": PagamentoViewSchema, "404": ErrorSchema})
def get_pagamento(query: PagamentoBuscaSchema):
    """Faz a busca por um Pagamento a partir do seu Id.

    Retorna uma representação do Pagamento encontrado (se encontrado).
    """
    pagamento_id = query.id
    logger.debug(f"Coletando dados sobre o Pagamento #{pagamento_id}")

    # Cria conexão com a base para fazer a busca
    session = Session()

    # Busca por Id
    pagamento = session.query(Pagamento).filter(Pagamento.id == pagamento_id).first()

    if pagamento:
        logger.debug(f"Pagamento econtrado: #{pagamento_id}")
        return apresenta_pagamento(pagamento), 200
    else:
        error_msg = "Pagamento não encontrado na base :/"
        logger.warning(f"Erro ao buscar Pagamento #{pagamento_id}: {error_msg}")
        return {"mesage": error_msg}, 404


@app.delete('/pagamento', tags=[pagamento_tag],
            responses={"200": PagamentoDelSchema, "404": ErrorSchema})
def del_pagamento(query: PagamentoBuscaSchema):
    """Remove um Pagamento a partir do seu Id.

    Retorna uma mensagem de confirmação da remoção do Pagamento alvo.
    """
    pagamento_id = query.id
    logger.debug(f"Removendo dados sobre Pagamento #{pagamento_id}")

    # Cria conexão com a base para fazer a busca
    session = Session()
    
    # Buscando e removendo o Pagamento
    pagamento_a_remover: Pagamento = session.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    valor_a_descontar = pagamento_a_remover.valor
    pagamento_descricao = pagamento_a_remover.descricao
    foi_removido = session.query(Pagamento).filter(Pagamento.id == pagamento_id).delete()
    session.commit()

    if foi_removido:
        logger.debug(f"Removendo Pagamento #{pagamento_id}:'{pagamento_descricao}'")
        atualiza_cache_da_soma_pagamentos(-valor_a_descontar)
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Pagamento removido", "id": pagamento_id, "descricao": pagamento_descricao}
    else:
        error_msg = "Pagamento não encontrado na base :/"
        logger.warning(f"Erro ao remover Pagamento #{pagamento_id}:'{pagamento_descricao}': {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/soma_pagamentos', tags=[analise_tag],
         responses={"200": SomaPagamentosSchema, "404": ErrorSchema})
def soma_pagamentos():
    """Retorna a soma dos valores de todos os Pagamentos."""
    soma_pagamentos: float = cache.get('soma_pagamentos')
    valida_cache_da_soma_de_pagamentos(soma_pagamentos)
        
    if soma_pagamentos:
        logger.debug(f"Obtida a soma dos valores dos Pagamentos")
        return {"soma_pagamentos": soma_pagamentos}, 200
    else:
        error_msg = "Não foi possível obter a soma dos valores dos Pagamentos :/"
        logger.warning(error_msg)
        return {"mesage": error_msg}, 404


#  --------------------------------------------------------------------------------------
#  Funções auxiliares
#  --------------------------------------------------------------------------------------
def valida_cache_da_soma_de_pagamentos(soma_pagamentos):
    """ Verifica se existe valor da soma de Pagamentos no seu respectivo cache.
    Se não existir, calcula a soma e preenche o cache.
    
    Retorna soma de Pagamentos validada
    """
    if soma_pagamentos is None:
        session = Session()
        soma_pagamentos = session.query(func.sum(Pagamento.valor)).scalar()
        cache.set('soma_pagamentos', soma_pagamentos)
    return soma_pagamentos


def atualiza_cache_da_soma_pagamentos(valor):
    """ Atualiza cache da soma de Pagamentos de acordo com o 'valor' fornecido."""
    soma_pagamentos: float = cache.get('soma_pagamentos')
    soma_pagamentos = valida_cache_da_soma_de_pagamentos(soma_pagamentos)
    cache.set('soma_pagamentos', soma_pagamentos + valor)
