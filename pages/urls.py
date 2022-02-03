from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('housesdata/', views.getJsonHouseData, name='housesdata'),
    path('house/', views.house, name='house')
]