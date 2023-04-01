from django.http import HttpResponse
from django.urls import path

from server.apps.identity.intrastructure.django.decorators import (
    redirect_logged_in_users,
)


@redirect_logged_in_users()
def sample_view(request):
    """A sample view that uses the decorator."""
    return HttpResponse('Test view')


def login_redirect_view(request):
    """A view that redirects to the login page."""
    return HttpResponse('Login Redirect View')


# Create a temporary Django URL pattern for testing purposes
urlpatterns = [
    path('sample_view/', sample_view, name='sample_view'),
    path('login_redirect/', login_redirect_view, name='login_redirect_view'),
]
