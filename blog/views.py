from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render

from blog.models import Post

class HomeView(TemplateView):
    template_name = 'home.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context
home = HomeView.as_view()

class ListPostsView(ListView):
    model = Post
    http_method_names = ['get']
    template_name = 'list_posts.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super(ListPostsView, self).get_context_data(**kwargs)
        adjacent_pages = 2
        page_number = context['page_obj'].number
        num_pages = context['paginator'].num_pages
        start_page = max(page_number - adjacent_pages, 1)
        if start_page <= 3:
            start_page = 1
        end_page = page_number + adjacent_pages + 1
        if end_page >= num_pages - 1:
            end_page = num_pages + 1
        page_numbers = [n for n in xrange(start_page, end_page) \
                if n > 0 and n <= num_pages]
        context.update({
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            })
        return context
list_posts = ListPostsView.as_view()

class ShowPostView(DetailView):
    model = Post
    http_method_names = ['get']
    template_name = 'show_post.html'
    context_object_name = 'post'
show_post = ShowPostView.as_view()
