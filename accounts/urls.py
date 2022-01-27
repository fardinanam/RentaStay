from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('addhome/', views.addhome, name='addhome'),
    path('fetch_states/<str:key>/', views.fetch_states, name='fetch_states'),
]
