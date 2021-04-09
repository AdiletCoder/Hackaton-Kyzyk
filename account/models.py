from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now


class AuthToken(models.Model):
    TOKEN_TYPE_REGISTER = 'register'
    TOKEN_TYPE_PASSWORD_RESET = 'password_reset'
    TOKEN_TYPE_CHOICES = (
        (TOKEN_TYPE_REGISTER, 'Регистрация'),
        (TOKEN_TYPE_PASSWORD_RESET, 'Восстановление пароля')
    )

    token = models.UUIDField(verbose_name='Токен', default=uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='tokens', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    life_days = models.IntegerField(default=7, verbose_name='Срок действия (в днях)')
    type = models.CharField(max_length=20, choices=TOKEN_TYPE_CHOICES,
                            default=TOKEN_TYPE_REGISTER, verbose_name='Тип токена')

    @classmethod
    def get_token(cls, token):
        try:
            return cls.objects.get(token=token)
        except cls.DoesNotExist:
            return None

    def is_alive(self):
        return (self.created_at + timedelta(days=self.life_days)) >= now()

    def __str__(self):
        return f'{self.user.name}'

    class Meta:
        verbose_name = 'Аутентификационный токен'
        verbose_name_plural = 'Аутентификационные токены'
