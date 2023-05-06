from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('process_image',views.process_image_view, name='process_image'),
]