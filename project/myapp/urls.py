from django.conf.urls import url
import myapp.views
from django.urls import path
urlpatterns = [
    path(r'login', myapp.views.login, ),
    path(r'regist', myapp.views.regist, ),
]
