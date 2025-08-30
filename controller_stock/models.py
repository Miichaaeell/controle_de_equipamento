from django.db import models
from equipment.models import Equipment
from controllers.models import UserTracking, TimeStampModel
from django.contrib.auth.models import User


class Location(TimeStampModel):
    TYPE_CHOICES = [
        ('estoque', 'Estoque'),
        ('cliente', 'Cliente'),
        ('tecnico', 'Técnico'),
    ]
    location = models.CharField(max_length=124, verbose_name='Local')
    type = models.CharField(
        max_length=124, verbose_name='Tipo', choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             verbose_name='Técnico', related_name='locations', null=True, blank=True)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'
        ordering = ['location']

    def __str__(self) -> str:
        return str(self.location)


class Reason(TimeStampModel):
    reason = models.CharField(max_length=124, verbose_name='Motivo')

    class Meta:
        verbose_name = 'Motivo'
        ordering = ['reason']

    def __str__(self):
        return self.reason


class ControllerStock(UserTracking, TimeStampModel):
    equipment = models.OneToOneField(
        Equipment, on_delete=models.PROTECT, verbose_name='Equipamento', related_name='stocks',)
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, verbose_name='Local', related_name='stocks')
    reason = models.ForeignKey(
        Reason, on_delete=models.PROTECT, verbose_name='Motivo', related_name='controllers')
    observation = models.TextField(
        verbose_name='Observação', default='Estoque')

    class Meta:
        verbose_name = 'Controle Estoque'
        verbose_name_plural = 'Controle Estoque'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['location'])
        ]

    def __str__(self):
        return f'{self.equipment}, {self.location}'


class Tracking(UserTracking, TimeStampModel):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.PROTECT, verbose_name='Equipamento', related_name='trackings')
    origin = models.ForeignKey(
        Location, on_delete=models.PROTECT, verbose_name='Origem', related_name='origins_trackings')
    destination = models.ForeignKey(
        Location, on_delete=models.PROTECT, verbose_name='Destino', related_name='destination_trackings')
    reason = models.ForeignKey(
        Reason, on_delete=models.PROTECT, verbose_name='Motivo', related_name='trackings')
    observation = models.TextField(
        verbose_name='Observação', default='Estoque')

    class Meta:
        verbose_name = 'Rastreio'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.equipment}'
