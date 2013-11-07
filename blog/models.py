from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse_lazy

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    image = models.ImageField(upload_to='posts', blank=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('show_post', kwargs={'slug': self.slug})
