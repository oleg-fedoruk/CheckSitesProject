from django.urls import path, include
from .views import *

urlpatterns = [
    path('', SitesListView.as_view(), name='home'),
    path('view/<int:pk>', SiteDetailView.as_view(), name='site_view'),
    path('new', CreateSite.as_view(), name='site_new'),
    path('edit/<int:pk>', UpdateSite.as_view(), name='site_edit'),
    path('delete/<int:pk>', DeleteSite.as_view(), name='site_delete'),
]
