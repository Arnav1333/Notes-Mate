from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.upload_note, name='upload_note'),
    path('list/', views.note_list, name='note_list'),
    path('',views.home,name='home'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)