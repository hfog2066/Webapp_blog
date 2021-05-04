from background_task.models import Task
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm
from .tasks import disable_or_publish_posts

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/signup', views.sign_up, name='signup'),
    path('auth/login', auth_views.LoginView.as_view(template_name='auth/login.html', authentication_form=LoginForm), name='login'),
    path('posts', views.PostListView.as_view(), name='posts/list'),
    path('posts/create', views.PostCreateView.as_view(), name='posts/create'),
    path('posts/update/<int:pk>', views.PostUpdateView.as_view(), name='posts/update'),
    path('posts/delete/<int:pk>', views.PostDeleteView.as_view(), name='posts/delete'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post/detail'),
    path('posts/<int:pk>/like', views.like_post, name='like')
]

if not Task.objects.filter(verbose_name='publications_task').exists():
    disable_or_publish_posts(repeat=60, verbose_name='publications_task')