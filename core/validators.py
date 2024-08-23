import phonenumbers
from django.core.exceptions import ValidationError

from core.utils import calculate_age


def validate_phone_number(value):
    if not str(value).isdecimal() and len(str(value)) < 9:
        try:
            parsed_number = phonenumbers(parsed_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Invalid phone number format.")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number format.")


def validate_birth_date(value):
    if value:
        age = calculate_age(value)
        if age < 18 or age > 60:
            raise ValidationError("Age must be between 18 and 60 years old.")
        

def validate_passwords(password, confirm_password):
    if password and confirm_password and password != confirm_password:
        raise ValidationError("Passwords do not match.")
