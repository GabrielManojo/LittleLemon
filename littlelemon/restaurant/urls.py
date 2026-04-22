from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    # Add the remaining URL path configurations here
    path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.display_menu_items, name="menu_item"),
    # API routes for Insomnia/testing clients.
    path('api/menu', views.api_menu, name='api_menu'),
    path('api/menu/<int:pk>', views.api_menu_detail, name='api_menu_detail'),
    path('api/bookings', views.api_bookings, name='api_bookings'),
    path('api/bookings/<int:pk>', views.api_booking_detail, name='api_booking_detail'),

]