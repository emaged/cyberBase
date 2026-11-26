from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('transfer/', views.transferView, name='transfer'),
    path('balance/', views.balanceView, name='balance'),
    path('book/', views.addressBookView, name='book'),
]
