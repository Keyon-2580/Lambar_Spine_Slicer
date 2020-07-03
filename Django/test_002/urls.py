"""test_002 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from demo import views as views
from . import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("api/", include("demo.urls")),
    #path("test/", views.test),
    path("login/", views.login),
    path("refresh/", views.refresh),
    path("delete/", views.delete),
    path("record/", views.record),
    path("add_patient/", views.add_patient),
    path("postfile/", views.postFile),
    path("temporaryfile/", views.temporaryFile),
    path("opinion/", views.opinion),
    path("read_img/",views.read_img),
    #path("readsplitimg/",views.readSplitImg),

    path("segmentation/",views.segmentation),
    path("", TemplateView.as_view(template_name="index.html")),
    path("models/",views.models),
    path("taosuo/",views.taosuo),
    path("dealed/",views.dealed),
    path("regist/",views.regist)


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
