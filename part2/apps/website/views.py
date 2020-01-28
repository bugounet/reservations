from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def index_view(request):
    """ Index view. This is reserved to authenticated users. Others are
    redirected to login screen.

    Index displays bookings and existing resources.
    """
    user = request.user
    return render(request, "website/index.html", {
        'user': user,
    })


def logout_view(request):
    logout(request)
    return redirect('login')
