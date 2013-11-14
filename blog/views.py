from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView)

from blog.models import Post

class PaginatePostsView(ListView):
    queryset = Post.objects.order_by('-created_on')
    context_object_name = 'posts'

class HomeView(PaginatePostsView):
    template_name = 'blog/home.html'
    http_method_names = ['get']
    paginate_by = 10
home = HomeView.as_view()

class AboutView(TemplateView):
    template_name = 'blog/about.html'
    http_method_names = ['get']
about = AboutView.as_view()

class ShowPostView(DetailView):
    model = Post
    http_method_names = ['get']
    template_name = 'show_post.html'
    context_object_name = 'post'
show_post = ShowPostView.as_view()

class NewPostView(CreateView):
    model = Post
    template_name_suffix = '_new_form'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(NewPostView, self).dispatch(*args, **kwargs)
new_post = NewPostView.as_view()
