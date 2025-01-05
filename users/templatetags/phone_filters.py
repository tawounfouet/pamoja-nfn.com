from django import template
import phonenumbers

register = template.Library()

@register.filter(name='phone_format')
def phone_format(phone_number):
    """
    Formate un numéro de téléphone pour l'affichage
    Ex: +33 6 12 34 56 78
    """
    try:
        parsed = phonenumbers.parse(str(phone_number))
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except:
        return phone_number 