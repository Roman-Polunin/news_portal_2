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
from django.urls import path, include
from news.views import BaseView, PostList, PostListSearch, AuthorList, CategoryList, CommentList, NewsList, PostListDetail, ArticleList, ContactsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authors/', AuthorList.as_view()),
    path('posts/', PostList.as_view()),
    path('news/', NewsList.as_view()),
    path('articles/', ArticleList.as_view()),
    path('posts/<int:pk>', PostListDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('comments/', CommentList.as_view()),
    path('', BaseView.as_view()),
    path('contacts/', ContactsView.as_view()),
    path('posts/search/', PostListSearch.as_view()),
]
