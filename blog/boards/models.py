from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    disable_date = models.DateTimeField(null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    publication_date = models.DateTimeField(blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(verbose_name="Creation date", auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
            update_fields=None):
        if not self.id and (self.publication_date and self.publication_date < timezone.now()):
            self.is_active = True
            super(Post, self).save()
        elif self.id and not self.is_disabled and (self.publication_date and self.publication_date < timezone.now()):
            self.is_active = True
            super(Post, self).save()
        else:
            super(Post, self).save()

    def like(self):
        self.likes += 1
        self.save()
        return self.likes

    def get_absolute_url(self):
        return reverse('post/detail', args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('creation_date',)


class Commentary(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=320)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentaries')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text