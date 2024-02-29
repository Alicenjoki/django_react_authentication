from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('token/', MyTokenObtainView.as_view() ),
    path('token/refresh/', TokenRefreshView.as_view() ),
    path('register/', RegisterView.as_view() ),
    path('dashboard/', Dashboard, name='dashboard' ),
]
