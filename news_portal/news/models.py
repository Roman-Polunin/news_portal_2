

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django import forms


class Author(models.Model):  # наследуемся от класса Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user}'

    def update_rating(self):
        posts = Post.objects.filter(author_id=self.id)
        comment_all = Comment.objects.all()
        cnt_posts = len(posts)
        comment_self_post_rtg = 0
        if Post.objects.filter(author_id=self.id).exists():
            post_rtg = Post.objects.filter(author_id=self.id).aggregate(models.Sum('post_rating'))['post_rating__sum']
        else:
            post_rtg = 0

        if comment_all.filter(user_id=self.user.id).exists():
            comment_self_rtg = comment_all.filter(user_id=self.user.id).aggregate(models.Sum('comment_rating'))['comment_rating__sum']
        else:
            comment_self_rtg = 0

        for i in range(cnt_posts):
            if comment_all.filter(post_id=posts[i].id).exists():
                comment_self_post_rtg += int(comment_all.filter(post_id=posts[i].id).aggregate(models.Sum('comment_rating'))['comment_rating__sum'])


        self.author_rating = post_rtg * 3 + comment_self_rtg + comment_self_post_rtg
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


post_type = [(0, 'news'), (1, 'article')]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.IntegerField(choices=post_type, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.TextField(max_length=255)
    post_text = models.TextField(max_length=15000)
    post_rating = models.IntegerField(default=1)


    def __str__(self):
        return f'{self.author}, {self.title}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating > 1:
            self.post_rating -= 1
        self.save()

    def preview(self):
        if len(self.post_text) > 124:
            preview_text = str(self.post_text[0:123] + '...')
        else:
            preview_text = self.post_text
        return preview_text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}, {self.post}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=255)
    date_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user}, {self.post}, {self.comment_text}'

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        if self.comment_rating > 1:
            self.comment_rating -= 1
        self.save()


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )