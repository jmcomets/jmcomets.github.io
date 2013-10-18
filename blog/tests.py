from django.test import TestCase

from blog.models import Post

class PostTest(TestCase):
    def test_slugify_title(self):
        test_posts = (
                ('this is a simple title', 'this-is-a-simple-title'),
                ('this_is_a_slugged_title', 'this_is_a_slugged_title'),
                )
        for title, slug in test_posts:
            post = Post(title=title)
            post.save()
            self.assertEqual(post.slug, slug)
