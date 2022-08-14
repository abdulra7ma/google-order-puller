# Django imports
from django.utils.translation import gettext_lazy as _


class ModelConstants:
    EMAIL = "email address"
    FIRST_NAME = "First name (as shown in ID)"
    MIDDLE_NAME = "Middle name (as shown in ID)"
    SURNAME = "Surname (as shown in ID)"
    PHONE_NUMBER = ""
    BIRTHDAY = ""
    CITY = ""
    IS_ACTIVE = "Account Activation status"
    IS_FROZEN = "Account frozen status"
    IS_STAFF = "Is Staff"

    CITY_MAX_LENGHT = 90


ModelConst = ModelConstants()
