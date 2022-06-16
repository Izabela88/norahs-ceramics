from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from customer.models import User
from django.core.validators import RegexValidator
from django.core.validators import validate_email


class UpdatePersonalInformationForm(forms.ModelForm):
    """
    Regex validator doesn't allow special characters but it will allow also
    special French, German, Polish, Italian, Spanish, Swedish, Norvegian,
    Danish, Russian, Ukrainian, Serbian, Bulgarian, Belarusian
    letters.
    """

    only_letters = RegexValidator(
        (
            "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
            "a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ"
            "a-zA-ZäöüßÄÖÜ"
            "a-zA-ZàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ"
            "a-zA-ZáéíñóúüÁÉÍÑÓÚÜ"
            "a-zA-ZäöåÄÖÅ"
            "a-zA-ZæøåÆØÅ"
            "а-яА-ЯёЁ"
            "а-щА-ЩЬьЮюЯяЇїІіЄєҐґ"
            "А-ИК-ШЂЈ-ЋЏа-ик-шђј-ћџ"
            "а-ъьюяА-ЪЬЮЯ"
            "ёа-зй-шы-яЁА-ЗЙ-ШЫІіЎў"
            "a-zA-ZĂÂÎȘȚăâîșț]*$"
        ),
        "No special characters and numbers allowed!",
    )

    phone_number = PhoneNumberField()
    first_name = forms.CharField(
        max_length=100, required=True, validators=[only_letters]
    )
    last_name = forms.CharField(
        max_length=100, required=True, validators=[only_letters]
    )
    email = forms.EmailField(
        max_length=254, required=True, validators=[validate_email]
    )

    class Meta:
        model = User
        fields = [
            "phone_number",
            "email",
            "first_name",
            "last_name",
        ]
