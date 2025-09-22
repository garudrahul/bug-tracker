from django.urls import path
from . import views

urlpatterns = [
    path('', views.bug_list, name="bug_list"),
    path('create/', views.bug_create, name="bug_create"),
    path('<int:bug_id>/edit/', views.bug_edit, name="bug_edit"),
    path('<int:bug_id>/delete/', views.bug_delete, name="bug_delete"),
    # path('register/', views.register, name="register"),
]