from django.urls import path
from .views import RoleView, add_role_to_user, remove_role_from_user, listing_privileges_bestowed_on_a_role, \
    listing_all_users_associated_with_a_role

urlpatterns = [

    path("roles", RoleView.as_view(), name="get"),
    path("roles/del/<int:pk>", RoleView.as_view(), name="delete-role"),
    path("roles/edit/<int:pk>", RoleView.as_view(), name="update-role"),
    path("add-role", add_role_to_user, name="add_role_to_user"),
    path("remove-role", remove_role_from_user, name="remove_role_from_user"),
    path(
        "list-pri",
        listing_privileges_bestowed_on_a_role,
        name="listing_privileges_bestowed_on_a_role",
    ),
    path('list-users-with-roles', listing_all_users_associated_with_a_role,
         name='listing_all_users_associated_with_a_role')

]
