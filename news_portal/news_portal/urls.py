"""news_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from news.views import BaseView, PostList, PostListSearch, AuthorList, CategoryList, CommentList, NewsList, PostListDetail, ArticleList, ContactsView, \
    NewsCreate, ArticleCreate, PostUpdate, NewsDelete, ArticleDelete, BaseRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('allauth.urls')),
    path('authors/', AuthorList.as_view()),
    path('posts/', PostList.as_view(), name='post_list'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticleList.as_view(), name='articles_list'),
    path('posts/<int:pk>', PostListDetail.as_view(), name='post_detail'),
    path('categories/', CategoryList.as_view()),
    path('comments/', CommentList.as_view()),
    path('', BaseView.as_view()),
    path('contacts/', ContactsView.as_view()),
    path('posts/search/', PostListSearch.as_view()),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('articles/create/', ArticleCreate.as_view(), name='post_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('accounts/login/', LoginView.as_view(template_name = 'account/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name = 'account/logout.html'), name='logout'),
    path('accounts/signup/', BaseRegisterView.as_view(template_name = 'account/signup.html'), name='signup'),
]
