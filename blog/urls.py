from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
        url(r'^$', 'home', name='home'),
        url(r'^posts/new', 'new_post', name='create_post'),
        url('r^posts/show/(?P<slug>[-_\w+])', 'show_post', name='show_post'),
        )
