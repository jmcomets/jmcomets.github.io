from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('blog.views',
        url(r'^$', 'home', name='home'),
        url('r^posts/(?P<slug>[-_\w+])', 'show_post', name='show_post'),
        )
