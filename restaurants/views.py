from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from products.models import ConsumableIncome, CheckoutProduct, ReportConsmable
from restaurants.mixins import ConsMixin, ConsListMixin, ConsDetailMixin, ResultMixin, RestDateMixin

from .forms import ConsumableIncomeFormSet, ConsumableIncomeUpdateFormSet, CheckoutProductFormSet, \
    CheckoutProductUpdateFormSet, \
    DateForm, ReportConsFormSet
from .models import Restaurant


class RestarauntListView(ListView):
    model = Restaurant


class RestarauntDetailView(ResultMixin, DetailView):
    model = Restaurant


class OrderCreate(CreateView):
    object = None
    template_name = "products/consumableincome_form.html"
    form_class = DateForm
    model = ConsumableIncome

    def get_context_data(self, *args, **kwargs):
        context = super(OrderCreate, self).get_context_data(*args, **kwargs)
        context["formset"] = kwargs["formset"] if "formset" in kwargs else ConsumableIncomeFormSet()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = ConsumableIncomeFormSet(request.POST)
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
        return HttpResponseRedirect(reverse('order_detail', kwargs={'slug': rest.slug, 'date': date}))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class OrderListView(ListView):
    model = ConsumableIncome

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data()
        orders = self.object_list
        dates = orders.values('date').distinct()
        context['dates'] = dates
        context['slug'] = self.kwargs.get('slug')
        return context


class OrderDetailView(UpdateView):
    object = None
    template_name = "products/consumableincome_update.html"
    fields = ['date']
    model = ConsumableIncome

    def get_initial(self):
        initial = super(OrderDetailView, self).get_initial()
        initial['date'] = self.kwargs['date']
        return initial

    def get_queryset(self):
        rest = get_object_or_404(Restaurant, slug=self.kwargs['slug'])
        date_str = self.kwargs['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')
        orders = ConsumableIncome.objects.all()
        qs = orders.filter(date=date, restaurant=rest)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        context["formset"] = kwargs["formset"] if "formset" in kwargs else ConsumableIncomeUpdateFormSet(
            queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = ConsumableIncomeUpdateFormSet(request.POST)
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
        return HttpResponseRedirect(reverse('order_detail', kwargs={'slug': rest.slug, 'date': date}))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class CheckoutProductCreate(CreateView):
    object = None
    template_name = "products/checkoutproduct_form.html"
    fields = ['date']
    model = CheckoutProduct

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutProductCreate, self).get_context_data(*args, **kwargs)
        context["formset"] = kwargs["formset"] if "formset" in kwargs else CheckoutProductFormSet()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = CheckoutProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        rest = Restaurant.objects.get(slug=self.kwargs['slug'])
        date = form.cleaned_data.get('date')
        for f in formset:
            self.object = f.save(commit=False)
            self.object.date = date
            self.object.restaurant = rest
            if self.object.amount and self.object.product:
                self.object.save()
        return HttpResponseRedirect(reverse('checkout', kwargs={'slug': rest.slug}))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class CheckoutProductListView(ListView):
    model = CheckoutProduct

    def get_context_data(self, **kwargs):
        context = super(CheckoutProductListView, self).get_context_data()
        products = self.object_list
        dates = products.values('date').distinct()
        context['dates'] = dates
        context['rest'] = self.kwargs['slug']
        return context


class CheckoutProductDetailView(RestDateMixin, UpdateView):
    object = None
    template_name = "products/checkoutproduct_update.html"
    fields = ['date']
    model = CheckoutProduct

    def get_initial(self):
        initial = super(CheckoutProductDetailView, self).get_initial()
        initial['date'] = self.kwargs['date']
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutProductDetailView, self).get_context_data(*args, **kwargs)
        context["formset"] = kwargs["formset"] if "formset" in kwargs else CheckoutProductUpdateFormSet(
            queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = CheckoutProductUpdateFormSet(request.POST)
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
            if self.object.amount and self.object.product:
                self.object.save()
        formset.save()
        return HttpResponseRedirect(reverse('checkout', kwargs={'slug': rest.slug}))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ReportCreate(ConsMixin, CreateView):
    model = ReportConsmable
    template_name = "products/reportcons_form.html"
    form_class = DateForm
    formset = ReportConsFormSet

    def get_success_url(self):
        return reverse('reports', kwargs={'slug': self.kwargs.get('slug')})


class ReportListView(ConsListMixin, ListView):
    model = ReportConsmable


class ReportDetailView(RestDateMixin, ConsDetailMixin, UpdateView):
    model = ReportConsmable
    fields = ['date']
    formset = ReportConsFormSet
    template_name = "products/reportcons_update.html"

    def get_success_url(self):
        date_str = self.kwargs['date']
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return reverse('reports', kwargs={'slug': self.kwargs.get('slug')})

        # def get_context_data(self, **kwargs):
        #     context = super(ReportDetailView, self).get_context_data(**kwargs)
        #     qs = context['formset'].queryset
        #     context['formset_qs'] = zip(context['formset'], qs)
        #     x = dict([(x[0].id, x[3]) for x in context.get('result')])
        #     y = dict(self.get_queryset().values_list('consumable__id', 'amount'))
        #     dicts = [x, y]
        #     c = Counter()
        #     for d in dicts:
        #         c.update(d)
        #     delta = dict(c)
        #     context['delta'] = delta
        #     return context


class ResultView(RestDateMixin, ResultMixin, ListView):
    model = ReportConsmable
    template_name = "restaurants/result.html"
