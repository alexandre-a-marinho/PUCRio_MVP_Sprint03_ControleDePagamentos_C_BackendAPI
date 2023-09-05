from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_caching import Cache
from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from model import Session, Payment
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Payments Control", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Sets cache
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Defining tags
home_tag = Tag(name="Documentation", description="Documentation selection: Swagger, Redoc or RapiDoc")
payment_tag = Tag(name="Payment", description="Addition, visualization, edition and deletion of payments from the database")
analysis_tag = Tag(name="Analysis", description="Statistics and analysis regarding the payments in the database")


#  --------------------------------------------------------------------------------------
#  Routes
#  --------------------------------------------------------------------------------------
@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, allowing us to chose the type od documentation."""
    return redirect('/openapi')


@app.post('/payment', tags=[payment_tag],
          responses={"200": PaymentViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_payment(form: PaymentSchema):
    """Adds a new Payment to the database.

    Returns the representation of the added Payment (as per PaymentViewSchema).
    """
    payment = Payment(
        description = form.description,
        category = form.category,
        subcategory = form.subcategory,
        value = form.value,
        nb_installments = form.nb_installments,
        insertion_date = date.today())
    # TODO: [1] Feature: allow user to add custom date
    
    logger.debug(f"Added Payment is described by: '{payment.description}'")
    try:
        # Creates database connection
        session = Session()

        # Adds new item to the database table and commits it
        session.add(payment)
        session.commit()
        logger.debug(f"Added Payment is described by: '{payment.description}'")
        value_to_add = form.value
        updates_payments_sum_cache(value_to_add)
        return show_payment(payment), 200

    except IntegrityError as e:
        error_msg = "Integrity error on new Payment addition :/"
        logger.warning(f"Error while adding Payment #{payment.id}({payment.description}): {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # in case of a non-expected error
        error_msg = "It was not possible to save the new Payment :/"
        logger.warning(f"Error while adding Payment #{payment.id}({payment.description}): {error_msg}")
        return {"message": error_msg}, 400


@app.put('/paymentedition', tags=[payment_tag],
          responses={"200": PaymentViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_payment(query: PaymentSearchSchema, form: PaymentSchema,):
    """Edits an existing Payment in the database.

    Returns the representation of the edited Payment (as per PaymentViewSchema).
    """
    edited_payment_id = query.id
    logger.debug(f"Edited Payment is described by: '#{edited_payment_id}({form.description})'")
    
    try:
        # Creates database connection
        logger.debug(f"Editing Payment #{edited_payment_id}")
        session = Session()
        
        # Selects item to edit it in the database table and then commits it
        database_payment_to_edit = session.query(Payment).filter(Payment.id == edited_payment_id).first()
        old_value = database_payment_to_edit.value;
        database_payment_to_edit.description = form.description
        database_payment_to_edit.category = form.category
        database_payment_to_edit.subcategory = form.subcategory
        database_payment_to_edit.value = form.value
        database_payment_to_edit.nb_installments = form.nb_installments
        database_payment_to_edit.insertion_date = date.today()
        session.commit()

        # Updates Sum of values
        value_to_add = (form.value - old_value)
        updates_payments_sum_cache(value_to_add)
        
        return show_payment(database_payment_to_edit), 200

    except IntegrityError as e:
        error_msg = "Integrity error on new Payment addition :/"
        logger.warning(f"Error while editing Payment #{database_payment_to_edit.id}({database_payment_to_edit.description}): {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # in case of a non-expected error
        error_msg = "It was not possible to save the new Payment :/"
        logger.warning(f"Error while editing Payment #{database_payment_to_edit.id}({database_payment_to_edit.description}): {error_msg}")
        return {"message": error_msg}, 400


@app.get('/payments', tags=[payment_tag],
         responses={"200": PaymentsListSchema, "404": ErrorSchema})
def get_payments():
    """Searches for all registered Payments.

    Returns the representation of a list of all registred Payments (if any exists).
    """
    logger.debug(f"Getting Payments")
    
    # Creates database connectio to perform the search
    session = Session()
    payments = session.query(Payment).all()

    if payments:
        logger.debug(f"%d Payments found" % len(payments))
        print(payments)
        updates_payments_sum_cache(0)
        # retuns the representation of the list of all payments found
        return show_payments(payments), 200
    else:
        # retorno empty if nothing is found
        return {"payments": []}, 200


@app.get('/payment', tags=[payment_tag],
         responses={"200": PaymentViewSchema, "404": ErrorSchema})
def get_payment(query: PaymentSearchSchema):
    """Searches a Payment based on it's Id.

    Returns the representation of a Payment (if found).
    """
    payment_id = query.id
    logger.debug(f"Getting Payment data #{payment_id}")

    # Creates database connectio to perform the search
    session = Session()

    # Searchs using payment Id
    payment = session.query(Payment).filter(Payment.id == payment_id).first()

    if payment:
        logger.debug(f"Payment found: #{payment_id}")
        return show_payment(payment), 200
    else:
        error_msg = "Payment not found in database :/"
        logger.warning(f"Erro while searching for Payment #{payment_id}: {error_msg}")
        return {"message": error_msg}, 404


@app.delete('/payment', tags=[payment_tag],
            responses={"200": PaymentDelSchema, "404": ErrorSchema})
def del_payment(query: PaymentSearchSchema):
    """Deletes a Payment based on it's Id.

    Returns a message confirming target Payment deletion.
    """
    payment_id = query.id
    logger.debug(f"Deleting Payment #{payment_id}")

    # Creates database connection to perform the search
    session = Session()
    
    # Searching and deleting target Payment
    payment_to_delete: Payment = session.query(Payment).filter(Payment.id == payment_id).first()
    value_to_discount = payment_to_delete.value
    payment_description = payment_to_delete.description
    payment_deletion_success = session.query(Payment).filter(Payment.id == payment_id).delete()
    session.commit()

    if payment_deletion_success:
        logger.debug(f"Payment deleted #{payment_id}:'{payment_description}'")
        updates_payments_sum_cache(-value_to_discount)
        # retuns the representation of the confirmation message
        return {"message": "Payment deleted", "id": payment_id, "description": payment_description}
    else:
        error_msg = "Payment not found in database :/"
        logger.warning(f"Error while deleting Payment #{payment_id}:'{payment_description}': {error_msg}")
        return {"message": error_msg}, 404


@app.get('/payments_sum', tags=[analysis_tag],
         responses={"200": PaymentsSumSchema, "404": ErrorSchema})
def payments_sum():
    """Returns the sum of value field from all database Payments."""
    payments_sum: float = cache.get('payments_sum')
    validates_payments_sum_cache(payments_sum)
        
    if payments_sum:
        logger.debug(f"Got sum of values from all Payments in the database")
        return {"payments_sum": payments_sum}, 200
    else:
        error_msg = "It was not possible to obtain the sum of Payment values:/"
        logger.warning(error_msg)
        return {"message": error_msg}, 404


#  --------------------------------------------------------------------------------------
#  Auxiliary functions
#  --------------------------------------------------------------------------------------
def validates_payments_sum_cache(payments_sum):
    """ Checks if there is a value of the sum of Payments in its respective cache.
    If it does not exist, it calculates the sum and fills the cache.
    
    Returns validate sum of Payments
    """
    if payments_sum is None:
        session = Session()
        payments_sum = session.query(func.sum(Payment.value)).scalar()
        cache.set('payments_sum', payments_sum)
    return payments_sum


def updates_payments_sum_cache(value):
    """ Updates cache of the sum of Payments according to the provided 'value'."""
    payments_sum: float = cache.get('payments_sum')
    payments_sum = validates_payments_sum_cache(payments_sum)
    cache.set('payments_sum', payments_sum + value)
