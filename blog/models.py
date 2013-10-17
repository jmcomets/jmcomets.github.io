from django.db import models
from django.template.defaultfilters import slugify

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    image = models.ImageField(upload_to='posts')
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
