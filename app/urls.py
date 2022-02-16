"""softwarecenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app import views

app_name = "app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("index/", views.IndexView.as_view(), name="index"),
    path("history/", views.HistoryView.as_view(), name="history"),
    path("upload/", views.UploadView.as_view(), name="upload"),
    path("download/<target>/", views.DownloadFileView.as_view(), name="download"),
    path("delete/<target>/", views.DeleteFileView.as_view(), name="delete"),
]
