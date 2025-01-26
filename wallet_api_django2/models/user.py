from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError(_('CPF é obrigatório'))

        user = self.model(
            cpf=cpf,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, password, **extra_fields)

class User(AbstractUser):
    username = None
    cpf = models.CharField(
        _('CPF'),
        max_length=11,
        unique=True,
        help_text=_('Apenas números')
    )
    full_name = models.CharField(_('Nome Completo'), max_length=255)
    email = models.EmailField(_('E-mail'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return self.full_name or self.cpf