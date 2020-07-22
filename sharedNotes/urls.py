from django.urls import path
from . import views

app_name = "sharedNotes"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('create/<int:note_id>', views.create, name="index"),
    path('<unique_id>', views.shared, name="index"),
]
