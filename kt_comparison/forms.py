from django import forms


class DateForm(forms.Form):
    from_date_month = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "from-date"}
        ),
    )
    to_date_month = forms.DateField(
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
    checkbox_tm = forms.BooleanField(
        required=False, label='Keitaro_1', widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    checkbox_tw = forms.BooleanField(
        required=False, label='Keitaro_2', widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )