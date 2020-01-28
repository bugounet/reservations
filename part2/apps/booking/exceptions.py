from django.utils.translation import ugettext_lazy as _


class BRException(
    Exception):
    pass


class CannotCancelPastBooking(BRException):
    def __init__(self):
        super(CannotCancelPastBooking, self).__init__(
            _("Cannot cancel past booking")
        )
