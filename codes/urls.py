from django.urls import path
from .views import new_code, lists

urlpatterns = [
    path('new/', new_code, name="new-code"),
    path('lists/', lists, name="lists"),
]
