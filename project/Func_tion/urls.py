from django.conf.urls import url
import Func_tion.views
from django.urls import path
urlpatterns = [
    path(r'func2', Func_tion.views.func2, ),
    path(r'function1', Func_tion.views.function1, ),
    path(r'function3', Func_tion.views.function3, ),
    path(r'function4', Func_tion.views.function4, ),
    path(r'func2_1', Func_tion.views.func2_1, ),
    path(r'function_get', Func_tion.views.function_get, ),
    path(r'function_get2', Func_tion.views.function_get2, ),
    path(r'function_get3', Func_tion.views.function_get3, ),
    path(r'function5', Func_tion.views.function5, ),
]
