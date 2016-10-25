from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from products.forms import QuantityFormSet, ConsFormSet
from products.models import Quantity, Product, Consumable
from restaurants.models import Restaurant

from src.products.forms import ProductFormSet
from .mixins import FormsetMixin


class ProductCreateVeiw(FormsetMixin, CreateView):
    model = Product
    fields = ['name']
    formset = QuantityFormSet

    def get_queryset(self):
        qs = super(ProductCreateVeiw, self).get_queryset()
        return qs.none()

    def form_valid(self, form, formset):
        slug = self.kwargs.get("slug")
        if slug:
            rest = get_object_or_404(Restaurant, slug=slug)
        self.object = form.save()
        self.object.restaurants.add(rest)
        self.object.save()
        formset.save(commit=False)
        for form in formset:
            if form.cleaned_data:
                new_item = form.save(commit=False)
                # if new_item.title:
                product = self.object
                new_item.product = product
                new_item.save()
        return HttpResponseRedirect(reverse('products', kwargs={'slug': slug}))


class ProductListView(FormsetMixin, UpdateView):
    model = Product
    formset = ProductFormSet
    fields = []
    template_name = "products/product_list.html"

    def get_object(self, queryset=None):
        return None

    def get_queryset(self):
        rest = Restaurant.objects.filter(slug=self.kwargs.get('slug'))
        qs = Product.objects.filter(restaurants=rest)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        qs = context['formset'].queryset
        context['formset_qs'] = zip(context['formset'], qs)
        context['slug'] = self.kwargs.get('slug')
        return context

    def form_valid(self, form, formset):
        formset.save()
        return HttpResponseRedirect("/")


class QuantityListView(FormsetMixin, UpdateView):
    model = Product
    fields = ['name', ]
    formset = QuantityFormSet
    template_name = "products/quantity_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(QuantityListView, self).get_context_data(*args, **kwargs)
        qs = Quantity.objects.filter(product=self.get_object())
        context["formset"] = kwargs["formset"] if "formset" in kwargs else self.formset(queryset=qs)
        return context

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.save(commit=False)
        for f in formset:
            new_obj = f.save(commit=False)
            if f.cleaned_data:
                new_obj.product = self.object
                new_obj.save()
        for obj in formset.deleted_objects:
            obj.delete()

        return HttpResponseRedirect(reverse('products', kwargs={'slug': self.kwargs.get('slug')}))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(QuantityListView, self).post(request, *args, **kwargs)


class ConsCreateView(FormsetMixin, CreateView):
    object = None
    model = Consumable
    fields = []
    formset = ConsFormSet

    def get_queryset(self):
        qs = super(ConsCreateView, self).get_queryset()
        return qs.none()

    def form_valid(self, form, formset):
        formset.save()
        return HttpResponseRedirect('/')


class ConsUpdateView(FormsetMixin, CreateView):
    object = None
    model = Consumable
    fields = []
    formset = ConsFormSet

    def form_valid(self, form, formset):
        formset.save()
        return HttpResponseRedirect('/')
