from django import forms
from django.forms import ModelForm, modelformset_factory

from products.models import Quantity, Consumable, Product


class QuantityForm(ModelForm):
    class Meta:
        model = Quantity
        fields = [
            "consumable",
            "amount",
        ]

        widgets = {
            'consumable': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


QuantityFormSet = modelformset_factory(Quantity, form=QuantityForm, extra=1, can_delete=True)

ConsFormSet = modelformset_factory(Consumable, fields=('name',), extra=0)

ProductFormSet = modelformset_factory(Product, fields=(), extra=0, can_delete=True)
