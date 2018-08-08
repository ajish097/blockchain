from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='index'),
    path('logout/',views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('transaction/', views.transaction_view, name='transaction'),
    path('', views.blockchain_view, name='blockchain'),
]