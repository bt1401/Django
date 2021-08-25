from django.urls import path
from .views import IndexClass,HomeClass, LoginClass,AddPost, AdminView, TestDetailView, UpdatePost, DeletePost
from.import views


app_name = 'mysite'
urlpatterns = [
    path('index/', IndexClass.as_view(), name="index"),
    path('', HomeClass.as_view(), name='home'),
    path('login/', LoginClass.as_view(), name="login"),
    path ('addpost/', AddPost.as_view(), name='add_post'),
    path ('testview/<int:pk>', TestDetailView.as_view(), name="test-view"), 
    path('admin-site/', AdminView.as_view(), name="admin-site"),
    path('update/edit/<int:pk>', UpdatePost.as_view(), name="update_post"),
    path('delete/<int:pk>/remove', DeletePost.as_view(), name="delete_post"),
    path('scrape/', views.home, name="scrape"),

    
    
]