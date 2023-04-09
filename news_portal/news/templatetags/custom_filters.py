from django import template
from news.models import *

register = template.Library()

cenzor_list = ['fake', 'fake news', 'обзор']

@register.filter()
def cenzor(value):
   """Проверка текста на запрещенные слова из списка"""
   temp_list = str(value).split()
   new_value = ""
   for word in temp_list:
      if word.lower() in cenzor_list:
         new_value += word[0]
         for i in range(len(word)-1):
            new_value += "*"
      else:
         new_value += word
      new_value += " "
   value = new_value[:-1]
   return f'{value} '

@register.filter()
def update_author_rating(self):
   """Обновление рейтинга автора"""
   self.update_rating()
   self.save()
   return self.author_rating

