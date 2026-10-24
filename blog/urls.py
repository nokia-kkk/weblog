from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rooms/', views.rooms, name='rooms'),
    path('elements/', views.elements, name='elements'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_details, name='blog_details'),
    path('blog/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]
