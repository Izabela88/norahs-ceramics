from django import forms


class FilterForm(forms.Form):

    min_price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": "1",
                "max": "150",
                "id": "min",
                "value": "1",
                "class": "range",
            }
        ),
        required=False,
    )

    max_price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": "1",
                "max": "150",
                "value": "150",
                "id": "max",
                "class": "range",
            }
        ),
        required=False,
    )
