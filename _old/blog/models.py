from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse_lazy

def validate_no_commas(value):
    if ',' in value:
        raise ValidationError('%s contains commas' % value)

class Category(models.Model):
    title = models.CharField(max_length=80,
            unique=True, validators=[validate_no_commas])

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    image = models.ImageField(upload_to='posts', blank=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=True)
    content = models.TextField()
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ('created_on',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        super(Post, self).save(*args, **kwargs)

    def get_slug(self):
        return self.slug or slugify(self.title)

    def get_absolute_url(self):
        return reverse_lazy('blog:show_post', kwargs={'slug': self.slug})
