class FormsetMixin(object):
    formset = None
    object = None

    def get_context_data(self, *args, **kwargs):
        context = super(FormsetMixin, self).get_context_data(*args, **kwargs)
        context["formset"] = kwargs["formset"] if "formset" in kwargs else self.formset(queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.formset(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
