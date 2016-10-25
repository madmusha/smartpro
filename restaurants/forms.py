from django import forms
from django.forms import ModelForm, formset_factory
from django.forms.models import modelformset_factory
from products.models import ConsumableIncome, CheckoutProduct, ReportConsmable


class DateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ConsumableIncome
        fields = ['date']

        labels = {
            'date': 'Дата'
        }


class ConsumableIncomeForm(ModelForm):
    class Meta:
        model = ConsumableIncome
        fields = ['consumable', 'amount']

        widgets = {
            'consumable': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount > 10000:
            raise forms.ValidationError(u"Количесвто должно быть меньше 10000")
        else:
            return amount


ConsumableIncomeFormSet = formset_factory(form=ConsumableIncomeForm, extra=1)
ConsumableIncomeUpdateFormSet = modelformset_factory(ConsumableIncome, form=ConsumableIncomeForm, extra=1,
                                                     can_delete=True)


class CheckoutProductForm(ModelForm):
    class Meta:
        model = CheckoutProduct
        fields = ['product', 'amount']

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


CheckoutProductFormSet = formset_factory(form=CheckoutProductForm, extra=1)
CheckoutProductUpdateFormSet = modelformset_factory(CheckoutProduct, form=CheckoutProductForm, extra=1, can_delete=True)


class ReportConsForm(ModelForm):
    class Meta:
        model = ReportConsmable
        fields = ['consumable', 'amount']

        widgets = {
            'consumable': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


ReportConsFormSet = modelformset_factory(ReportConsmable, form=ReportConsForm, extra=1, can_delete=True)
