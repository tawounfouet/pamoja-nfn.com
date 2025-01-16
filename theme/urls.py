


from django.urls import path
from . import views
from .views import index

urlpatterns = [
    # path('', views.home, name='home'),
    path('', index, name='index'),
    path('home1/', views.home1, name='home1'),

]