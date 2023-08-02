from django.urls import include, path
from propylon_document_manager.file_versions.api import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('file-upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('file-retrieve/', views.FileRetrieveView.as_view(), name='file-retrieve'),
]
