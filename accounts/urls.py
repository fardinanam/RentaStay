from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('deleteprofile/', views.deleteprofile, name='deleteprofile'),
    path('addhome/', views.addhome, name='addhome'),
    path('homepreview/<int:house_id>/', views.homepreview, name='homepreview'),
    path('fetch_statenames/<str:key>/', views.fetch_statenames, name='fetch_statenames'),
    path('fetch_citynames/<str:key1>/<str:key2>/', views.fetch_citynames, name='fetch_citynames'),
    path('fetch_no_of_house_pics/<int:house_id>/', views.fetch_no_of_house_pics, name='fetch_no_of_house_pics'),
    path('addroom/<int:house_id>/', views.addroom, name='addroom'),
    path('roompreview/<int:house_id>/<int:roomnumber>/', views.roompreview, name='roompreview'),
    path('fetch_no_of_room_pics/<int:house_id>/<int:roomnumber>/', views.fetch_no_of_room_pics, name='fetch_no_of_room_pics'),
    path('edithouseinfo/<int:house_id>/', views.edithouseinfo, name='edithouseinfo'),
    path('editroominfo/<int:house_id>/<int:roomnumber>/', views.editroominfo, name='editroominfo'),
]
