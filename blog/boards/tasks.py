from background_task import background
from django.utils import timezone

from .models import Post


@background(schedule=1)
def disable_or_publish_posts(repeat=180, verbose_name='publications_task'):
    next_activations = Post.objects.filter(publication_date__lt=timezone.now(), is_active=False, is_disabled=False)
    next_disabilities = Post.objects.filter(disable_date__isnull=False, disable_date__lt=timezone.now(), is_active=True)
    next_activations.update(is_active=True)
    next_disabilities.update(is_active=False, is_disabled=True)