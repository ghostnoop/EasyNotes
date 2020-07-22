from django.urls import path, include
from . import views
from .views import AjaxHandlerView
import sharedNotes.views as snote

app_name = "notes"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('', views.index, name="index"),

    path("signup/", views.sign_up, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),

    path('create/', views.create, name='create'),
    path('board/', views.board, name='board'),

    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('settings/', views.settings, name='settings'),

    path('del_note/<int:note_id>/', views.del_note, name='del_note'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),

    path('ajax', AjaxHandlerView.as_view()),

    path('share/create/<int:note_id>', snote.create, name="snote_create"),
    path('share/<unique_id>', snote.shared, name="snote_shared")
    # path('share/', include("sharedNotes.urls")),
    # path('<int:algorithm_id>/', views.detail, name='detail'),
    # path('<int:algorithm_id>/leave_comment/', views.leave_comment, name='leave_comment'),
]
