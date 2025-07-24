from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from .serializers import *
from .models import *
from random import randint
from time import sleep
from rest_framework.views import APIView
from rest_framework.response import Response


def code_generate(length: int) -> str:
    code: str = ''
    for symbol in range(length):
        code += randint(0, 9)
    return code


class TelephoneNumberRequestView(APIView):
    def post(self,
             request, ):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            pass

        profile, created = Profile.objects.get_or_create(phone_number=phone_number)

        code = randint(1000, 9999)
        print(profile)
        profile.auth_code = code_generate(4)
        profile.save()

        sleep(2)

        return Response({"auth_code": code})


class VerifyCodeView(APIView):
    def post(self,
             request, ):
        phone_number = request.data.get('phone_number')
        entered_code = request.data.get('code')

        try:
            profile = Profile.objects.filter(phone_number=phone_number)
        except:
            return Response({"error": "Invalid phone number"})

        if profile.auth_code != entered_code:
            return Response({"error": "Invalid code"})

        if not profile.is_authenticated:
            profile.is_authenticated = True

            while True:
                inv_code = code_generate(6)
                if not Profile.objects.filter(invite_code=inv_code).exists():
                    profile.invite_code = inv_code
                    break

            entered_inv_code = request.data.get('entered_inv_code')

            if entered_inv_code:
                try:
                    inviter = Profile.objects.get(invite_code=entered_inv_code)
                    profile.invited_by = inviter
                except:
                    pass

            profile.save()

        return Response({"message": "Verified", "invite_code": profile.invite_code})


class ProfileView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        try:
            profile = Profile.objects.get(phone_number=phone_number)
        except:
            return Response({"error": "User not found"})

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        entered_inv_code = request.data.get('inv_code')

        try:
            profile = Profile.objects.get(phone_number=phone_number)
        except:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if entered_inv_code:
            try:
                inviter = Profile.objects.get(invite_code=entered_inv_code)
                if not profile.invited_by:
                    profile.invited_by = inviter
                    profile.save()
            except:
                return Response({"error": "Invite code not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

