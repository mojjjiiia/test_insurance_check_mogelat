from django import forms


class CheckForm(forms.Form):
    POLIS_TYPES = [
        ('OMS', 'OMS'),
        ('DMS', 'DMS'),
    ]

    polis_type = forms.ChoiceField(choices=POLIS_TYPES)
    company = forms.CharField(max_length=255)
    polis_number = forms.CharField(max_length=50)
    services = forms.CharField(max_length=1024)
