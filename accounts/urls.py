from django.urls import path
from .views import user_login, user_logout, account_edit, account_edit_password

urlpatterns = [
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('account/edit', account_edit, name="account-edit"),
    path('account/edit-password', account_edit_password, name="account-edit-password"),
]

