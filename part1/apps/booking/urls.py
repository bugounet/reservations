from django.urls import path
from apps.booking.views import BookingListView, BookingDetailsView

urlpatterns = [
    path(
        'booking/<int:pk>',
        BookingDetailsView.as_view(),
        name="booking_details"
    ),
    path('bookings', BookingListView.as_view(), name="bookings_list"),
]
