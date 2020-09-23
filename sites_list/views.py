from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Site


class SitesListView(ListView):
    model = Site
    template_name = 'home.html'
    context_object_name = 'sites'


class SiteDetailView(DetailView):
    model = Site
    template_name = 'site_view.html'


class CreateSite(CreateView):
    model = Site
    template_name = 'site_new.html'
    fields = ['title', 'site', 'is_active']
    success_url = reverse_lazy('home')


class UpdateSite(UpdateView):
    model = Site
    template_name = 'site_form.html'
    fields = ['title', 'site', 'is_active']
    success_url = reverse_lazy('home')


class DeleteSite(DeleteView):
    model = Site
    template_name = 'site_delete.html'
    success_url = reverse_lazy('home')
