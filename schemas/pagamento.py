from pydantic import BaseModel
from typing import List
from model.pagamento import Pagamento
from datetime import date

#  --------------------------------------------------------------------------------------
#  Schemas
#  --------------------------------------------------------------------------------------
class PagamentoSchema(BaseModel):
    """Define como um novo Pagamento deve ser representado na inserção"""
    descricao: str = "inscrição maratona do Rio"
    categoria: str = "Esportes"
    subcategoria: str = "Corrida"
    valor: float = 160.0
    num_parcelas: int = 1
    data_insercao: date = date(2023, 4, 10)


class PagamentoBuscaSchema(BaseModel):
    """Define a estrutura da requisição de busca por Pagamentos.

    Deve ser utilizado o Id do pagamento.
    """
    id: int = 5


class ListagemPagamentosSchema(BaseModel):
    """Define como uma lista de Pagamentos será retornada."""
    pagamentos: List[PagamentoSchema]


class PagamentoViewSchema(BaseModel):
    """Define a estrutura de retorno de um Pagamento."""
    id: int = 1
    descricao: str = "inscrição maratona do Rio"
    categoria: str = "Esportes"
    subcategoria: str = "Corrida"
    valor: float = 160.0
    num_parcelas: int = 1
    data_insercao: date = date(2023, 4, 10)


class PagamentoDelSchema(BaseModel):
    """Define a estrutura do retorno de uma requisição de remoção de Pagamento."""
    message: str = "Informações sobre sucesso ou falha na remoção"
    id: int = 5
    descricao: str = "inscrição maratona do Rio"
    
class SomaPagamentosSchema(BaseModel):
    """Define estrutura do retorno da soma do 'Valor' da tabela Pagamentos."""
    soma_pagamentos: float = 2568.35
    

#  --------------------------------------------------------------------------------------
#  Funções auxiliares
#  --------------------------------------------------------------------------------------
def apresenta_pagamentos(pagamentos: List[Pagamento]):
    """Retorna uma representação de um conjunto de Pagamentos."""
    result = []
    for pagamento in pagamentos:
        result.append({
            "id": pagamento.id,
            "descricao": pagamento.descricao,
            "categoria": pagamento.categoria,
            "subcategoria": pagamento.subcategoria,
            "valor": pagamento.valor,
            "num_parcelas": pagamento.num_parcelas,
            "data_insercao": pagamento.data_insercao
            })

    return {"pagamentos": result}

def apresenta_pagamento(pagamento: Pagamento):
    """ Retorna representação de um Pagamento segundo PagamentoViewSchema."""
    return {
        "id": pagamento.id,
        "descricao": pagamento.descricao,
        "categoria": pagamento.categoria,
        "subcategoria": pagamento.subcategoria,
        "valor": pagamento.valor,
        "num_parcelas": pagamento.num_parcelas,
        "data_insercao": pagamento.data_insercao
    }
