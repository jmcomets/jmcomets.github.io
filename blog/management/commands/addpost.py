from optparse import make_option
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from blog.models import Category, Post
from _private import get_external_content

class Command(BaseCommand):
    args = '<post_title>'
    help = 'Add a new post without accessing the web interface'

    option_list = BaseCommand.option_list + (
        make_option('-c', '--categories',
            type='string', default='',
            help='Specify the post\'s categories, separated by commas'),
        )

    def handle(self, title, *args, **options):
        post = Post(title=title)

        # category read by csv
        category_title_list = options['categories'].split(',')
        for category_title in category_title_list:
            if not category_title:
                continue
            category_title = category_title.lower()
            try:
                category = Category.objects.get(title__iexact=category_title)
                categories.append(category)
            except Category.DoesNotExist:
                raise CommandError('Category "%s" does not exist' % category_title)

        # content read from external program
        try:
            post.content = get_external_content()
        except IOError as e:
            raise CommandError(e)

        # validate and save
        try:
            post.save()
        except IntegrityError as e:
            print 'Post cannot be created, reason: %s' % e
