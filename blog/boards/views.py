from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.base import ContextMixin
from django_filters.views import FilterView

from .filters import PostFilter
from .forms import *


class NavigationEnabled(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(NavigationEnabled, self).get_context_data(**kwargs)
        context['nav'] = True
        return context


class LoginRequired(LoginRequiredMixin):
    login_url = '/blog/auth/login'


def like_post(request, *args, **kwargs):
    if request.user.is_authenticated:
        likes = Post.objects.get(id=kwargs['pk']).like()
        return JsonResponse({'likes': likes})
    else:
        return HttpResponseForbidden()


class PostUpdateView(LoginRequired, UpdateView, NavigationEnabled):
    context_object_name = 'post'
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/posts/post_update.html'
    success_url = reverse_lazy('posts/list')

    def get_success_url(self):
        form = self.form_class()(self.request.POST)
        if form.is_valid():
            try:
                to_save = True if self.request.POST['save'] else False
                if to_save:
                    return reverse_lazy('posts/list')
            except Exception as e:
                print(e)
        return reverse_lazy('posts/update', args=[self.object.id])


class PostDetailView(LoginRequired, DetailView, NavigationEnabled):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['commentary_form'] = CreateCommentaryForm({'post_id': self.object.id})
        context['commentaries'] = self.object.commentaries.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.get_queryset())
        form = CreateCommentaryForm(self.request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.object
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            ctx = self.get_context_data(**kwargs)
            ctx.update({'form': form})
            return self.render_to_response(ctx)


class PostCreateView(LoginRequired, CreateView, NavigationEnabled):
    template_name = '/blog/posts/post_create.html'
    form_class = PostCreationForm
    success_url = reverse_lazy('posts/list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PostCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['author'] = self.request.user
        return kwargs


class PostListView(LoginRequired, FilterView, NavigationEnabled):
    filterset_class = PostFilter
    model = Post
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = '/blog/posts/post_list.html'
    ordering = ['-publication_date']

    def get_queryset(self):
        return Post.objects.filter(is_active=True, is_disabled=False).order_by('-publication_date')


class PostDeleteView(LoginRequired, DeleteView):
    model = Post
    success_url = reverse_lazy('posts/list')


def base(request):
    return render(request, 'base.html')


def home(request):
    return HttpResponseRedirect('posts')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['username'].lower()
            user.is_active = True
            print(user.__dict__)
            user.save()
            return redirect('posts/list')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form, 'nav': True})