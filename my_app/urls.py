from django.urls import path
from my_app import views

app_name = 'my_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('add_notes/', views.createNotes, name='add_notes'),
    path('update_notes/<str:pk>/', views.updateNotes, name='update_notes'),
    path('delete_notes/<str:pk>/', views.deleteNotes, name='delete_notes')
]
