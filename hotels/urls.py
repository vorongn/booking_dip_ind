from django.contrib import admin
from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [

    path('', views.index, name='home'),

    path('city/<slug:city_slug>/', views.show_category, name='category'),

    path('hotels/', views.HotelsList.as_view(), name='hotels_list'),

    path('hotels/<slug:hotel_slug>/', views.hotel_detail, name='hotel_detail'),

    path('hotels/<slug:hotel_slug>/<slug:room_slug>/', views.room_detail, name='room_detail'),

    path('book/', views.room_detail_book, name='room_detail_book'),

    path('book/my/', views.get_my_book, name='get_my_book'),

#-------------------------------------------------------------------
    path('addhotel/', views.AddHotel.as_view(), name='add_hotel'),
    path('edit/<slug:slug>/', views.UpdateHotel.as_view(), name='hotel_edit'),
    path('addroom/', views.AddRoom.as_view(), name='add_room'),
#-------------------------------------------------------------------
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),


]