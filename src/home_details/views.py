from django.shortcuts import render
from django.views.generic import TemplateView

from .froms import ContactForm


class HomePage(TemplateView):
    template_name = 'home_details/home-page.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        return context


class ContactPage(TemplateView):
    template_name = 'home_details/contact_page.html'
    contact_form = ContactForm

    def get_context_data(self, **kwargs):
        context = super(ContactPage, self).get_context_data(**kwargs)
        context['form'] = self.contact_form(self.request.POST or None)
        return context

    def post(self, request, **kwargs):
        contact_form = self.contact_form(request.POST or None)
        context = {
            'form': contact_form,
        }
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
        return render(request, self.template_name, context)
