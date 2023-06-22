from pydantic import BaseModel
from typing import List
from model.payment import Payment
from datetime import date

#  --------------------------------------------------------------------------------------
#  Schemas
#  --------------------------------------------------------------------------------------
class PaymentSchema(BaseModel):
    """Defines how a new Payment must be represented for database insertion"""
    description: str = "inscription to Rio Marathon"
    category: str = "Sports"
    subcategory: str = "Running"
    value: float = 160.0
    nb_installments: int = 1
    insertion_date: date = date(2023, 4, 10)


class PaymentSearchSchema(BaseModel):
    """Defines the structure of the requisition that searches for Payments.

    The search is made using the Payment Id.
    """
    id: int = 5


class PaymentsListSchema(BaseModel):
    """Defines how to return a Payments list."""
    payments: List[PaymentSchema]


class PaymentViewSchema(BaseModel):
    """Defines how to return a single Payment."""
    id: int = 1
    description: str = "inscription to Rio Marathon"
    category: str = "Sports"
    subcategory: str = "Running"
    value: float = 160.0
    nb_installments: int = 1
    insertion_date: date = date(2023, 4, 10)


class PaymentDelSchema(BaseModel):
    """Defines the structure of the requisition that deletes a Payment."""
    message: str = "Information regarding deletion success/failure"
    id: int = 5
    description: str = "inscription to Rio Marathon"
    
class PaymentsSumSchema(BaseModel):
    """Defines how to return the sum of 'values' from the Payments table."""
    payments_sum: float = 2568.35
    

#  --------------------------------------------------------------------------------------
#  Auxiliary functions
#  --------------------------------------------------------------------------------------
def show_payments(payments: List[Payment]):
    """Returns the representation of a group of Payments."""
    result = []
    for payment in payments:
        result.append({
            "id": payment.id,
            "description": payment.description,
            "category": payment.category,
            "subcategory": payment.subcategory,
            "value": payment.value,
            "nb_installments": payment.nb_installments,
            "insertion_date": payment.insertion_date
            })

    return {"payments": result}

def show_payment(payment: Payment):
    """Returns the representation of a Payment as per the PaymentViewSchema."""
    return {
        "id": payment.id,
        "description": payment.description,
        "category": payment.category,
        "subcategory": payment.subcategory,
        "value": payment.value,
        "nb_installments": payment.nb_installments,
        "insertion_date": payment.insertion_date
    }
