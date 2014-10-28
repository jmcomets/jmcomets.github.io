---
layout: post
title: Django magic
---

Since this morning I've been working on this website, which happens to be built
with [Django](https://www.djangoproject.com/). My goals, set at 10:30 today:

* setup a new database schema without losing (numerous) posts, mainly adding
  post categories (page *soon-to-be* available on the website)
* add some custom management commands, since I'm a __huge__ fan of
  [Vim](http://www.vim.org/) and I wanted to be able to blog without having
  access to internet, thus keeping local storage of unpublished posts
* add syntax highlighting using [google code prettifier](https://code.google.com/p/google-code-prettify/)

I am pleased to see that after 3 hours of lazy Sunday work, including
coffee/breakfast time, *all* these features are implemented.


Django really surprises me every single time with its simplicity of expression
(no wait that's Python :p), and the productivity rate when extending the basic
features.

Here's a snippet directly from the website's source code, adding a "categories"
command allowing me to easily list categories currently added:

{% highlight python %}
class Command(BaseCommand):
    help = 'List all categories'
    def handle(self):
          categories = Category.objects.all()
          if not categories:
              self.stdout.write('No categories available\n')
          else:
              self.stdout.write('Categories:\n')
          for category in categories:
              self.stdout.write('- %s\n' % category)
{% endhighlight %}

I don't know how this could be more explicit, and even so, this performs many
implicit actions which helps you focus on the important code rather than the
boilerplate. Here's what happens when calling this command:

0. __Command-line completion__: yup, this is definitely useful
1. Settings are read: using either the default settings in the manage.py
   script, or in the environment variable DJANGO\_SETTINGS\_MODULE. This way I
   can run this command either locally or on the deployment server. Note that
   the settings read can be overriden directly via the command-line arguments,
   by passing *--settings=dotted.path.to.settings*.
2. ORM magic: when accessing the model's manager through "Category.objects", I
   can easily change the behaviour when selecting all categories, without
   touching this code! I find this amazing in terms of code reuse.
3. Pretty error messages: exceptions are caught and nicely printed
4. Help messages: this command is automatically added to the manage.py's
   command list, grouped under the app's name. If I run "python manage.py help
   categories", I get the help message defined above "List all categories".

Cool huh ? :)

EDIT: this website is now hosted my Github pages, therefore runs on [Jekyll](http://jekyllrb.com/).
