from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.import_page),
    url(r'Home/$', views.home_page),
    url(r'Import/$', views.import_page),
    url(r'Search/$', views.search_page),
    url(r'Search/data1.json$', views.json_handler),

    url(r'About/$', views.post_form_upload),   # test page
    url(r'Import/upload_handler/$', views.upload_handler, name='upload_handler'),
    #url(r'^savetodb/$', savetodb, name="savetodb"),
)