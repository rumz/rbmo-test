from django import forms
from rbmo.models  import BudgetAllocation
from django.contrib.auth.models import User


class FundRequestForm(forms.Form):
    MONTHS = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'),
          (10, 'October'), (11, 'November'), (12, 'December'))

    month = forms.ChoiceField(choices=MONTHS,
                              widget=forms.Select(attrs={
                                  'class': 'form-control'
                              }
    ))
    amount = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control',
               'required': 'True'
        }
    ))

