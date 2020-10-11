from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .forms import DateTimeForm, SendMailForm
from .models import Site, Log
from .services import get_uptime_percent
from django.core.paginator import Paginator


class SitesListView(ListView):
    model = Site
    template_name = 'home.html'
    context_object_name = 'sites'


class SiteDetailView(View):

    def get(self, request, pk):
        site = Site.objects.get(id=pk)
        users_to_send_email = site.responsible_users.all()
        site_logs = Log.objects.filter(the_site=site).order_by('-created_at')
        uptime = get_uptime_percent(site_obj=site)
        date_time_form = DateTimeForm()
        send_mail_user_form = SendMailForm()

        paginator = Paginator(site_logs, 10)
        page = request.GET.get('page')
        site_logs = paginator.get_page(page)

        context = {'site': site, 'logs': site_logs, 'users_to_send_email': users_to_send_email,
                   'uptime': uptime, 'date_time': date_time_form,
                   'send_mail_form': send_mail_user_form,
                   }
        return render(request, 'site_view.html', context=context)

    def post(self, request, pk):
        site = Site.objects.get(id=pk)
        users_to_send_email = site.responsible_users.all()
        uptime = get_uptime_percent(site_obj=site)
        date_time_form = DateTimeForm(request.POST)
        send_mail_user_form = SendMailForm(request.POST)
        if date_time_form.is_valid():
            from_date_time = date_time_form.cleaned_data.get('from_date')
            till_date_time = date_time_form.cleaned_data.get('till_date')
            site_logs = Log.objects.filter(the_site=site,
                                           created_at__range=(from_date_time, till_date_time)
                                           ).order_by('-created_at')
            context = {'site': site, 'logs': site_logs, 'users_to_send_email': users_to_send_email,
                       'uptime': uptime, 'date_time': date_time_form,
                       'send_mail_form': send_mail_user_form,
                       }
            return render(request, 'site_view.html', context=context)

        elif send_mail_user_form.is_valid():
            user_id = send_mail_user_form.cleaned_data.get('send_mail_user')
            if 'user_selected' in request.POST:
                site.responsible_users.add(user_id)
            elif 'user_deleted' in request.POST:
                site.responsible_users.remove(user_id)
        return HttpResponseRedirect(self.request.path_info)


class CreateSite(CreateView):
    model = Site
    template_name = 'site_new.html'
    fields = ['title', 'site_url', 'is_active']
    success_url = reverse_lazy('home')


class UpdateSite(UpdateView):
    model = Site
    template_name = 'site_form.html'
    fields = ['title', 'site_url', 'is_active']
    success_url = reverse_lazy('home')


class DeleteSite(DeleteView):
    model = Site
    template_name = 'site_delete.html'
    success_url = reverse_lazy('home')
