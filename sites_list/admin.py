from django.contrib import admin
from sites_list.models import Site


class SiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'site', 'is_active']

    actions = ['check_site', 'dont_check_site']

    def check_site(self, request, queryset):
        count = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, '%s сайтов выделено для дальнейшей проверки.' % count)

    def dont_check_site(self, request, queryset):
        count = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(request, '%s сайтов выделено для снятия с проверки.' % count)

    check_site.short_description = "Поставить сайт(ы) на проверку"
    dont_check_site.short_description = "Снять сайт(ы) с проверки"


admin.site.register(Site, SiteAdmin)
