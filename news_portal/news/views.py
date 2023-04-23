from operator import concat

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import User, PermissionsMixin
from django.views.generic.edit import CreateView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

SERVER_EMAIL = os.getenv('DJ_SECRET_SERVER_EMAIL')
SERVER_HOST = os.getenv('DJ_SECRET_SERVER_HOST')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


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


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    permission_required = ('sign.add_news',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 0
        user = self.request.user
        super().form_valid(form)
       # отправляем письмо
        html_content = render_to_string(
            'news_created.html',
            {
                'appointment': post,
                'user': user,
                'link': f'{SERVER_HOST}{"posts/"}{post.pk}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{post.title} {post.date_create.strftime("%Y-%m-%d")}',
            body=f'{SERVER_HOST}{"posts/"}{post.pk} /'
                 f'{post.post_text}',
            from_email=SERVER_EMAIL,
            to=[SERVER_EMAIL, 'romanpolunin2511@yandex.ru'],

        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()

        # send_mail(
        #     subject=f'{post.title} {post.date_create.strftime("%Y-%m-%d")}',
        #     message=f'{"http://127.0.0.1:8000/posts/"}{post.pk} /'
        #             f'{post.post_text}',
        #     from_email=SERVER_EMAIL,
        #     recipient_list=[SERVER_EMAIL, 'romanpolunin2511@yandex.ru'],
        #     fail_silently=False,
        # )

        return super().form_valid(form)





class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    permission_required = ('sign.add_article',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 1
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('sign.update_post',)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('sign.delete_news',)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles_list')
    permission_required = ('sign.delete_article',)