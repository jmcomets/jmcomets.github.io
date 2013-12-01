import os
import subprocess
from tempfile import NamedTemporaryFile
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from blog.models import Category, Post

def get_external_content(filename=None, initial_content=''):
    """
    Read external content from the user's EDITOR, defaulting to vi. Initial
    content may be specified by giving a list of lines or a string to write at
    the beginning of the tmpfile created in the process.
    Raises an IOError if an error occured.
    """
    if filename:
        fp = open(filename, 'rw')
    else:
        fp = NamedTemporaryFile()
        filename = fp.name

    # write initial content
    if initial_content:
        if isinstance(initial_content, (list, tuple)):
            fp.writelines(initial_content)
        else:
            fp.write(initial_content)

    # edit tmpfile
    editor = os.environ.get('EDITOR', 'vi')
    if subprocess.call([editor, filename]) != 0:
        raise IOError('EDITOR exited with a non-zero status')

    return fp.read()

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

        # category
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

        # content
        try:
            post.content = get_external_content()
        except IOError as e:
            raise CommandError(e)

        post.save()
