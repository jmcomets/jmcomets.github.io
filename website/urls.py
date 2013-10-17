from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        # admin site
        url(r'^admin/', include(admin.site.urls)),

        # redirect to blog by default
        url(r'^$', RedirectView.as_view(url='/blog/')),
        )
