from django.utils.translation import ugettext_lazy as _


class BRException(Exception):
    pass


class CannotCancelPastBooking(BRException):
    def __init__(self):
        super(CannotCancelPastBooking, self).__init__(
            _("Cannot cancel past booking")
        )


class OverUsedResource(BRException):
    def __init__(self):
        super(OverUsedResource, self).__init__(
            _("Resource is over-used")
        )
