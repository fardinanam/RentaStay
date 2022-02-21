from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('housesdata/', views.getJsonHouseData, name='housesdata'),
    path('yourhousesdata/', views.getJsonYourHouseData, name='yourhousesdata'),
    path('house/<int:house_id>/', views.house, name='house'),
    path('housePhotosPath/<int:house_id>/', views.getJsonHousePhotosPath, name='housePhotosPath'),
    path('housePriceRange/<int:house_id>/', views.getJsonHousePriceRange, name='housePriceRange'),
    path('yourhouses/',views.yourhouses, name='yourhouses'),
    path('reservation/<int:house_id>/<int:room_no>/<str:check_in>/<str:check_out>/<int:guests>',
        views.reservation, name='reservation'),
    path('availableRooms/<int:house_id>/<str:check_in>/<str:check_out>/<int:guests>',
        views.getJsonAvailableRoomsData, name='availableRooms'),
    path('myRents/', views.myRents, name='myRents'),
    path('myGuests/', views.myGuests, name='myGuests'),
    path('updateReview/<int:rent_id>/<str:owner_rating>/<str:house_rating>/<str:owner_review>/<str:house_review>', views.updateReview, name='updateReview')
]