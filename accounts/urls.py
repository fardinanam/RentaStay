from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('addhome/', views.addhome, name='addhome'),
    path('homepreview/', views.homepreview, name='homepreview'),
    path('fetch_statenames/<str:key>/', views.fetch_statenames, name='fetch_statenames'),
    path('fetch_citynames/<str:key1>/<str:key2>/', views.fetch_citynames, name='fetch_citynames'),
]
