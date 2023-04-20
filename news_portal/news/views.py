from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class AuthorList(ListView):
    model = Author
    ordering = 'user'
    template_name = 'authors.html'
    context_object_name = 'authors'


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'categories.html'
    context_object_name = 'categories'


class PostList(ListView):
    model = Post
    ordering = '-date_create'
    #queryset = Post.objects.filter(type=1).order_by('-date_create')
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostListSearch(ListView):
    model = Post
    ordering = '-date_create'
    #queryset = Post.objects.filter(type=1).order_by('-date_create')
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class ArticleList(ListView):
    #model = Post
    #ordering = '-date_create'
    queryset = Post.objects.filter(type=1).order_by('-date_create')
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

class NewsList(ListView):
    #model = Post
    #ordering = '-date_create'
    queryset = Post.objects.filter(type=0).order_by('-date_create')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostListDetail(DetailView):
    model = Post
    #ordering = '-date_create'
    #queryset = Post.objects.filter(type=0).order_by('-date_create')
    template_name = 'post.html'
    context_object_name = 'post'




class CommentList(ListView):
    model = Comment
    ordering = 'date_create'
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 10


class BaseView(TemplateView):
    template_name = 'base.html'


class ContactsView(TemplateView):
    template_name = 'contacts.html'


class NewsCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 0
        return super().form_valid(form)


class ArticleCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 1
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles_list')