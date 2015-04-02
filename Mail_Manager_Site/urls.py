from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.import_page),
    url(r'Import/$', views.import_page),
    url(r'Import/upload_handler/$', views.upload_handler, name='upload_handler'),
    url(r'Search/$', views.search_page),
    url(r'Search/remove_row/$', views.remove_row_from_table)
)