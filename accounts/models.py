from django.contrib.auth.models import User


class CustomUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name']

    def __str__(self):
        return self.username
