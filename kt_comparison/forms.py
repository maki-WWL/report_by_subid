from django import forms


class DateForm(forms.Form):
    date_month = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "from-date"}
        ),
    )
    first_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "from-date"}
        ),
    )
    second_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "to-date"}
        ),
    )
