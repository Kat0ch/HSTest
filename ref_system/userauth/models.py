from django.db import models


class Profile(models.Model):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Телефон')
    auth_code = models.CharField(max_length=4, null=True, blank=True, verbose_name='Код авторизации')
    is_authenticated = models.BooleanField(default=False, verbose_name='Авторизован')
    invite_code = models.CharField(max_length=20, unique=True, verbose_name='Код приглашения')
    invited_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='invited_profiles', verbose_name='Кем приглашен')

    def __str__(self):
        return f'{self.is_authenticated} - {self.phone_number}'
