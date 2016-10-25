from datetime import datetime

from django.db.models import Case, IntegerField
from django.db.models import F
from django.db.models import Sum
from django.db.models import When
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from products.models import ReportConsmable, Consumable
from restaurants.models import Restaurant


class ConsMixin(object):
    object = None
    formset = None

    def get_queryset(self):
        qs = super(ConsMixin, self).get_queryset()
        return qs.none()

    def get_context_data(self, *args, **kwargs):
        context = super(ConsMixin, self).get_context_data(*args, **kwargs)
        context["formset"] = kwargs["formset"] if "formset" in kwargs else self.formset(queryset=self.get_queryset())
        context['slug'] = self.kwargs.get('slug')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.formset(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        rest = Restaurant.objects.get(slug=self.kwargs['slug'])
        date = form.cleaned_data.get('date')
        date_str = datetime.strftime(date, '%Y-%m-%d')
        for f in formset:
            x = f.is_valid()
            self.object = f.save(commit=False)
            self.object.date = date
            self.object.restaurant = rest
            if self.object.amount and self.object.consumable:
                self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ConsListMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ConsListMixin, self).get_context_data()
        reports = self.object_list
        dates = reports.values('date').distinct()
        context['dates'] = dates
        context['slug'] = self.kwargs.get('slug')
        return context


class ConsDetailMixin(object):
    object = None
    formset = None

    def get_initial(self):
        initial = super(ConsDetailMixin, self).get_initial()
        initial['date'] = self.kwargs['date']
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(ConsDetailMixin, self).get_context_data(*args, **kwargs)
        context["formset"] = kwargs["formset"] if "formset" in kwargs else self.formset(queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.formset(request.POST)
        formset.is_valid()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_object(self, queryset=None):
        return None

    def form_valid(self, form, formset):
        rest = Restaurant.objects.get(slug=self.kwargs['slug'])
        date = form.cleaned_data.get('date')
        date_str = datetime.strftime(date, '%Y-%m-%d')
        for f in formset:
            self.object = f.save(commit=False)
            self.object.date = date
            self.object.restaurant = rest
            if self.object.amount and self.object.consumable:
                self.object.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ResultMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ResultMixin, self).get_context_data()
        rest = get_object_or_404(Restaurant, slug=self.kwargs.get('slug'))
        rest_condition = Case(When(quantity__product__checkoutproduct__restaurant__id=rest.id, then=1), default=0,
                              output_field=IntegerField())
        result = Consumable.objects.annotate(
            minus=rest_condition * Coalesce(Sum('quantity__product__checkoutproduct__amount'), 0) * Coalesce(
                F('quantity__amount'), 0),
            plus=rest_condition * Coalesce(Sum('consumableincome__amount'), 0),
            check=rest_condition * Coalesce(Sum('reportconsumable__amount'), 0),
        )

        context['result'] = result

        return context


class RestDateMixin(object):
    def get_queryset(self):
        rest = get_object_or_404(Restaurant, slug=self.kwargs.get('slug'))
        date_str = self.kwargs['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')
        reports = ReportConsmable.objects.all()
        qs = reports.filter(date=date, restaurant=rest)
        return qs
