from django.urls import path
from . import views

urlpatterns = [
    path('file/', views.upload, name="upload file"),
    path('certificate/', views.upload, name="upload"),
    path('file/fileUpload/', views.fileUpload, name="file upload"),
    path('studentcertificates/', views.getStudentCertificate, name="upload"),
    path('certificates/', views.getStudentCertificate, name="cert folder"),
    path('certified/', views.getCertified, name="certify")
]

