from django.urls import path
from .views import new_code, lists, single_code\
    , category_list, single_code_edit, category_new, category_edit

urlpatterns = [
    path('category/', category_list, name="category-list"),
    path('category/new', category_new, name="category-new"),
    path('category/<int:pk>/edit', category_edit, name="category-edit"),
    path('new/', new_code, name="new-code"),
    path('<int:pk>/', single_code, name="single-code"),
    path('<int:pk>/edit/', single_code_edit, name="single-code-edit"),
    path('lists/', lists, name="lists"),
]
