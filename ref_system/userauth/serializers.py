from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    invited_users_phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['phone_number', 'auth_code', 'invite_code', 'invited_by']

    def get_invited_users_phone_numbers(self, obj):
        return [profile.phone_number for profile in obj.invited_users.all()]
