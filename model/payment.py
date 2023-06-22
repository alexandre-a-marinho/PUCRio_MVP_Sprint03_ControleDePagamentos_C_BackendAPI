from sqlalchemy import Column, String, Integer, Date, Float
from datetime import date
from typing import Union

from model import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = Column("pk_payment", Integer, primary_key = True)
    description = Column(String(140))
    category = Column(String(60))
    subcategory = Column(String(60))
    value = Column(Float)
    nb_installments = Column(Integer, default = 1)
    insertion_date = Column(Date, default = date.today())

    def __init__(self, description:str, category:str, subcategory:str, value:float,
                 nb_installments:int, insertion_date:Union[date, None] = None):
        """Creates a Payment.

        Arguments:
        description = description of the goods/services being paid for
        category = category of the goods/services being paid for (exs: Market, Sports, Restaurant, Trip, etc)
        subcategory = subcategory of the goods/services being paid for (ex: em Mercado: Hortifruti, Higiene, Açougue, etc)
        value: total value of the Payment, in Reais (R$). It's the sum of all installments
        nb_installments = number of monthly installments
        insertion_date: when the Payment was inserted in the database
        """
        self.description = description
        self.category = category
        self.subcategory = subcategory
        self.value = value
        self.nb_installments = nb_installments
        if insertion_date:
            self.insertion_date = insertion_date
