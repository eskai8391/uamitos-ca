from typing import Any, Optional, TypeVar, Callable

T = TypeVar('T')

class ValidationError(Exception):
    """Exception raised for validation errors in builder methods."""
    pass

def validate_not_none(param_value: Any, param_name: str) -> None:
    """
    Validates that a parameter is not None
    
    :param param_value: The value to validate
    :param param_name: The name of the parameter for error messages
    :raises ValidationError: If the parameter is None
    """
    if param_value is None:
        raise ValidationError(f"Parameter '{param_name}' cannot be None")

def validate_min_value(param_value: int, param_name: str, min_value: int) -> None:
    """
    Validates that a numeric parameter is greater than or equal to a minimum value
    
    :param param_value: The value to validate
    :param param_name: The name of the parameter for error messages
    :param min_value: The minimum allowed value
    :raises ValidationError: If the parameter is less than min_value
    """
    if param_value < min_value:
        raise ValidationError(f"Parameter '{param_name}' must be greater than or equal to {min_value}")

def validate_string_not_empty(param_value: str, param_name: str) -> None:
    """
    Validates that a string parameter is not empty
    
    :param param_value: The string value to validate
    :param param_name: The name of the parameter for error messages
    :raises ValidationError: If the string is empty
    """
    if param_value == "":
        raise ValidationError(f"Parameter '{param_name}' cannot be an empty string")

def validate_type(param_value: Any, param_name: str, expected_type: type) -> None:
    """
    Validates that a parameter is of the expected type
    
    :param param_value: The value to validate
    :param param_name: The name of the parameter for error messages
    :param expected_type: The expected type of the parameter
    :raises ValidationError: If the parameter is not of the expected type
    """
    if not isinstance(param_value, expected_type):
        raise ValidationError(
            f"Parameter '{param_name}' must be of type {expected_type.__name__}, got {type(param_value).__name__}"
        )

def validate_with_function(param_value: Any, param_name: str, validator_func: Callable[[Any], bool], 
                          error_msg: Optional[str] = None) -> None:
    """
    Validates a parameter using a custom validation function
    
    :param param_value: The value to validate
    :param param_name: The name of the parameter for error messages
    :param validator_func: A function that returns True if validation passes, False otherwise
    :param error_msg: Optional custom error message
    :raises ValidationError: If the validator function returns False
    """
    if not validator_func(param_value):
        message = error_msg if error_msg is not None else f"Parameter '{param_name}' failed validation"
        raise ValidationError(message)