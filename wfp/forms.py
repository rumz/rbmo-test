from django import forms
from rbmo.models  import BudgetAllocation, Allocation

class WFPForm(forms.ModelForm):
    activity = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'required' : 'True'
    }))

    allocation = forms.ModelChoiceField(queryset=Allocation.objects.all(),
                                   widget=forms.Select(attrs={
                                       'class' : 'form-control'
                                   })
    )

    performance_indicator = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'required' : 'True'
    }))

    q1 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    q2 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    q3 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    q4 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    jan = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    feb = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    mar = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    apr = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    may = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    jun = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    jul = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    aug = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    sept = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    oct = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    nov = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))

    dec = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))



    class Meta:
        model = BudgetAllocation
        fields = ['activity', 'allocation', 'performance_indicator', 'q1', 
                  'q2', 'q3', 'q4', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                  'jul', 'aug', 'sept', 'oct', 'nov', 'dec']
