from optparse import make_option
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from blog.models import Category

class Command(BaseCommand):
    help = 'Manage categories without accessing the web interface'
    specific_options = (
            make_option('--add', type='string', help='Add a new category'),
            make_option('--delete', type='string', help='Delete a category'),
            )
    option_list = BaseCommand.option_list + specific_options

    def handle(self, *args, **options):
        if 'add' in options and options['add']:
            try:
                Category.objects.create(title=options['add'])
            except IntegrityError as e:
                raise CommandError('Category cannot be created, reason: %s' % e)
        elif 'delete' in options and options['delete']:
            try:
                Category.objects.get(title=options['delete']).delete()
            except (IntegrityError, Category.DoesNotExist) as e:
                raise CommandError('Category cannot be deleted, reason: %s' % e)
        else:
            print 'Available "Category" management commands are:'
            for opt in self.specific_options:
                print '    %s: %s' % (opt, opt.help)
