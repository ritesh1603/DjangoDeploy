from django.urls import path
from . import views

#URLConf
urlpatterns = [
path('hello/', views.hello),
path('form/', views.form)
]