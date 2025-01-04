from django.urls import path
from . import views


urlpatterns = [
    path('', views.listings, name='listings'),
    path('<str:slug>', views.listing, name='listing'),
    path('create-listing/', views.createListing, name='create-listing'),
    path('update-listing/<str:slug>', views.updateListing, name='update-listing'),
    path('delete-listing/<str:slug>', views.deleteListing, name='delete-listing'),
    #path('delete-listing/<int:pk>', views.deleteListing, name='delete-listing'),

]