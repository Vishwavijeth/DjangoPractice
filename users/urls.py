from django.urls import path
from . import views

urlpatterns = [
    path('verify-email/', views.verify_email, name='verify_email'),
    path('verify-email/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
]
