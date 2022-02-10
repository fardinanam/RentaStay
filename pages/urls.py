from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('housesdata/', views.getJsonHouseData, name='housesdata'),
    path('house/<int:house_id>/', views.house, name='house'),
    path('housePhotosPath/<int:house_id>/', views.getJsonHousePhotosPath, name='housePhotosPath'),
    path('housePriceRange/<int:house_id>/', views.getJsonHousePriceRange, name='housePriceRange'),
]