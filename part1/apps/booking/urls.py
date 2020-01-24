from django.urls import path
from .views import BookingListView, BookingDetailsView, BookingCreationView

urlpatterns = [
    path(
        'new-booking',
        BookingCreationView.as_view(),
        name="create_booking_view"
    ),
    path(
        'booking/<int:pk>',
        BookingDetailsView.as_view(),
        name="booking_details"
    ),
    path('bookings', BookingListView.as_view(), name="bookings_list"),
]
