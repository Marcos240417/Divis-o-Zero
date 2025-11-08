# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # DEFINIÇÃO DOS PERFIS DE ACESSO
    ROLE_CHOICES = (
        ('USER', 'Usuário Cliente'),
        ('ADMIN', 'Administrador Técnico'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')  # [cite: 906]
    company_name = models.CharField(max_length=120, blank=True, null=True)  # [cite: 906]

    def is_admin(self):
        """Método auxiliar para checar permissão de administrador."""
        return self.role == 'ADMIN'  # [cite: 906]