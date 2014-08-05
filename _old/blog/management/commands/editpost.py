from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from blog.models import Category, Post
from _private import get_external_content

class Command(BaseCommand):
    args = '<post_title>'
    help = 'Edit a post without accessing the web interface'

    def handle(self, title, *args, **options):
        try:
            post = Post.objects.get(title__iexact=title)
        except Post.DoesNotExist:
            raise CommandError('Post "%s" does not exist' % title)

        # content read from external program
        try:
            post.content = get_external_content(initial_content=post.content)
        except IOError as e:
            raise CommandError(e)

        # validate and save
        try:
            post.save()
        except IntegrityError as e:
            print 'Post cannot be created, reason: %s' % e

