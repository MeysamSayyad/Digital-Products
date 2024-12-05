from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class PhoneNumberValidator(RegexValidator):
    regex = "^98(9[0-3,9]\d{8}[1-9]\d{9})$"
    message = "Phone number must be a VALID 12 digits like 98xxxxxxxxx"
    code = "invalid_phone_number"


class SKUValidator(RegexValidator):
    regex = "^[a-zA-Z0-9\-\_]{6,20}$"
    message = "SKU must be alphanumeric with 6 to 20 characters"
    code = "invalid_sku"


class UsernameValidator(RegexValidator):
    regex = "^[a-zA-Z][a-zA-Z0-9_\.]+$"
    message = _("Enter a valid username starting with a-z")
    code = "invalid_username"


class PostalCodeValidator(RegexValidator):
    regex = "^[0-9]{10}$"
    message = _("Enter a valid postal code")
    code = "invalid_postal_code"


class IDNumberValidator(RegexValidator):
    regex = "^[0-9]{10}$"
    message = _("Enter a valid id  number")
    code = "invalid_id_number"
