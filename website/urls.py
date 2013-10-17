from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        # admin app
        url(r'^admin/', include(admin.site.urls)),

        # redirect to blog by default
        url(r'^$', RedirectView.as_view(url='/blog/')),

        # other apps
        url(r'^blog/', include('blog.urls')),
        )

# fix for heroku deployment (serve static files)
if not settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                { 'document_root': settings.STATIC_ROOT }),
            )
