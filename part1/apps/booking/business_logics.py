from django.utils.timezone import now as tznow


class MetaInfos():
    def __init__(self, booking):
        self.booking = booking

    def is_over(self):
        return (self.booking.end_datetime < tznow())

    def is_ongoing(self):
        return (
            self.booking.start_datetime <= tznow() < self.booking.end_datetime
        )