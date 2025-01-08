from django.urls import path
from . import views

urlpatterns = [
    path('verify-email/', views.verify_email, name='verify_email')
]
