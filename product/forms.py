from django import forms


class FilterForm(forms.Form):

    min_price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": "1",
                "max": "150",
                "id": "min",
                "class": "range",
                "value": "1",
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
                "id": "max",
                "class": "range",
                "value": "150",
            }
        ),
        required=False,
    )

    category = forms.CharField(widget=forms.HiddenInput())
    sub_category = forms.CharField(widget=forms.HiddenInput())
