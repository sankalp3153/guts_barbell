from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('category/<slug:slug>/', views.CategoryBlogListView.as_view(), name='category_blogs'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
