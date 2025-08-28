from django.urls import path
from .views import (UserRegistrationView,ParagraphSubmissionView,WordSearchView,)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('paragraphs/submit/', ParagraphSubmissionView.as_view(), name='paragraph-submit'),
    path('paragraphs/search/', WordSearchView.as_view(), name='paragraph-search'),
]