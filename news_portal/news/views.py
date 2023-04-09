from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import *
from .filters import PostFilter

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