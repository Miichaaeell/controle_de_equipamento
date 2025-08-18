from django.db import models
from django.contrib.auth.models import User


class UserTracking(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.PROTECT,
                                    verbose_name='Responsável', related_name='%(class)s_changes')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.responsible:
            user = kwargs.pop('user', None)
            if user and user.is_authenticated:
                self.responsible = user
        super().save(*args, **kwargs)
        
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        abstract = True
