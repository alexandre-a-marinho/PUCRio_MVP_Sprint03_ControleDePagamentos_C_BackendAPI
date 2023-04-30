from sqlalchemy import Column, String, Integer, Date, Float
from datetime import date
from typing import Union

from model import Base


class Pagamento(Base):
    __tablename__ = 'pagamentos'

    id = Column("pk_pagamento", Integer, primary_key = True)
    descricao = Column(String(140))
    categoria = Column(String(60))
    subcategoria = Column(String(60))
    valor = Column(Float)
    num_parcelas = Column(Integer, default = 1)
    data_insercao = Column(Date, default = date.today())

    def __init__(self, descricao:str, categoria:str, subcategoria:str, valor:float,
                 num_parcelas:int, data_insercao:Union[date, None] = None):
        """Cria um Pagamento.

        Argumentos:
        descricao = descrição do que foi pago
        categoria = categoria do bem ou serviço pago (ex: Mercado, Esportes, Restaurante, Viagens, etc)
        subcategoria = subcategoria do bem ou serviço pago (ex: em Mercado: Hortifruti, Higiene, Açougue, etc)
        valor: valor total do Pagamento, em R$ (soma das parcelas) 
        num_parcelas = número de parcelas mensais
        data_insercao: data de quando o Pagamento foi inserido na base
        """
        self.descricao = descricao
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.valor = valor
        self.num_parcelas = num_parcelas
        if data_insercao:
            self.data_insercao = data_insercao
