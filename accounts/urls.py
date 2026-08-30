from django.urls import path
from . import views


urlpatterns = [

    # Register
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Login
    path(
        "login/",
        views.user_login,
        name="login"
    ),

    # Logout
    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    # Profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # Edit Profile
    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),
]