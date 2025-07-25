from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/number_request/', TelephoneNumberRequestView.as_view(), name='number_request'),
    path('api/verifycode/', VerifyCodeView.as_view(), name='verify_code'),
    path('api/view_profile/', ProfileView.as_view(), name='view_profile')
]