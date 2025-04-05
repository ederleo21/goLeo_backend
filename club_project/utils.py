from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Caracteres inválidos para un número de teléfono.")






