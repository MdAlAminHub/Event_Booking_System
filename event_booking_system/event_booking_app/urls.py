from django.urls import path
from .views import ListEventView, CreateEventView, BookEventView, UserBookingsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', ListEventView.as_view(), name='list-events'),
    path('events/create/', CreateEventView.as_view(), name='create-event'),
    path('events/book/', BookEventView.as_view(), name='book-event'),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
]
