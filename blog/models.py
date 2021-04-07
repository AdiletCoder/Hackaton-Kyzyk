from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} --> {self.title}'
        return self.title


class Post(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    image = models.ImageField(upload_to='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        return self.image.url

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-date_pub']


class ReviewPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentaries', verbose_name='Post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name='User')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def str(self):
        return f'{self.user}: {self.post}'

    class Meta:
        ordering = ['-created']
