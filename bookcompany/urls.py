from django.conf.urls import patterns, include, url
from views import *
import os.path
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#print os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')



urlpatterns = patterns('',
    (r'^$', homepage),
    (r'^home/$',home),
    (r'^home/order/$',order),
    (r'^home/book/$',book),
    (r'^home/bookorder/$',bookorder),
    (r'^home/bookorder/update/$',updateorder),
    (r'^home/bookorder/submit/$',submitorder),
    (r'^home/bookorder/add/$',addbook),
    (r'^home/account/$',account),
    (r'^home/login/$',  login),
    (r'^home/logout/$', logout),    
        # (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/images/')}),
        # (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/css/')}),
        # (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/js/')}),

    # Examples:
    # url(r'^$', 'bookcompany.views.home', name='home'),
    # url(r'^bookcompany/', include('bookcompany.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
