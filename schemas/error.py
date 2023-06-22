from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Defines how to represent an error message
    """
    message: str = "Details about the errors found"
