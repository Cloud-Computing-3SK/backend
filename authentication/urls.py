from django.urls import path
from .views import (register, login, CreateOrganizationView, CreateUserView, UserDetailView, ListOrganizationUsersView, 
                    AssignUserToOrganizationView, OrganizationDetailView, SearchUserView)

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('organizations/create/', CreateOrganizationView.as_view()),
    path('organizations/users/', ListOrganizationUsersView.as_view()),
    path('organizations/assign-user/<uuid:user_id>/', AssignUserToOrganizationView.as_view()),
    path('organizations/<uuid:org_id>/', OrganizationDetailView.as_view()),
    path('users/create/', CreateUserView.as_view()),
    path('users/search/', SearchUserView.as_view()),
    path('users/<uuid:user_id>/', UserDetailView.as_view()),
]
