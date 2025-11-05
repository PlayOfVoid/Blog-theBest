from django.urls import path
from . import views as blog

app_name = 'blog'

urlpatterns = [
    path('', blog.index, name='index'),
]