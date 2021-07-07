import re
from django.core.exceptions import ValidationError


def username_validation(name: str) -> None:
    r_expr = re.match('^[\w.@+-]+$', name)
    if r_expr == None:
        raise ValidationError(
            "String must contain only letters, digits and @/./+/-/_.")


def password_validation(name: str) -> None:
    r_expr = re.match('^(?=.*[A-Z])(?=.*\d).{8,}$', name)
    if r_expr == None:
        raise ValidationError(
            "Try to use other password.")
