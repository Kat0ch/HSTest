from django.urls import path, include
from .views import *

urlpatterns = [
    path('numberrequest/', TelephoneNumberRequestView.as_view(), name='number_request'),
    path('verifycode/', VerifyCodeView.as_view(), name='verify_code')
]