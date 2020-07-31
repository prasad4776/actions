from django.urls import path
from .views import AllUsers, AdminUser

urlpatterns = [
    path("user/<str:pk>/", AdminUser.as_view(), name="user-get-update"),
    path("user/all", AllUsers.as_view(), name="detail-list"),

]
