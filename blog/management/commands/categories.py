from optparse import make_option
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from blog.models import Category

class Command(BaseCommand):
    help = 'Manage categories without accessing the web interface'
    specific_options = (
            make_option('--add', type='string', help='Add a new category'),
            make_option('--delete', type='string', help='Delete a category'),
            make_option('--list', nargs=0, help='List all categories'),
            )
    option_list = BaseCommand.option_list + specific_options

    def handle(self, *args, **options):
        if 'add' in options and options['add']:
            try:
                Category.objects.create(title=options['add'])
            except IntegrityError as e:
                raise CommandError('Category cannot be created, reason: %s' % e)
            else:
                self.stdout.write('Category "%s" created' % options['add'])
        elif 'delete' in options and options['delete']:
            try:
                Category.objects.get(title=options['delete']).delete()
            except (IntegrityError, Category.DoesNotExist) as e:
                raise CommandError('Category cannot be deleted, reason: %s' % e)
            else:
                self.stdout.write('Category "%s" deleted' % options['deleted'])
        elif 'list' in options:
            categories = Category.objects.all()
            if not categories:
                self.stdout.write('No categories available\n')
            else:
                self.stdout.write('Categories:\n')
            for category in categories:
                self.stdout.write('- %s\n' % category)
        else:
            self.stdout.write('Available "Category" management commands are:\n')
            for opt in self.specific_options:
                self.stdout.write('    %s: %s\n' % (opt, opt.help))
