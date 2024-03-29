from django.urls import path
from my_app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'my_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('add_notes/', views.createNotes, name='add_notes'),
    path('notes/', views.viewNotes, name='notes'),
    path('update_notes/<str:pk>/', views.updateNotes, name='update_notes'),
    path('delete_notes/<str:pk>/', views.deleteNotes, name='delete_notes'),
    path('data/', views.getData, name="data"),
    path('load-more', views.loadMore, name="load-more"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)