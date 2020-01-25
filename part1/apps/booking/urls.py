from django.urls import path
from . import views

urlpatterns = [
    path(
        'new-booking',
        views.BookingCreationView.as_view(),
        name="create_booking_view"
    ),
    path(
        'booking/<int:pk>',
        views.BookingDetailsView.as_view(),
        name="booking_details"
    ),
    path(
        'bookings',
        views.BookingListView.as_view(),
        name="bookings_list"
    ),
]
