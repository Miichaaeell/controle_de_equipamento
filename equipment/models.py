from django.db import models
from controllers.models import TimeStampModel, UserTracking


class Branch(TimeStampModel):
    branch = models.CharField(
        max_length=124, unique=True, verbose_name='Marca')

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['branch']

    def __str__(self):
        return self.branch


class ModelEquipment(TimeStampModel):
    model = models.CharField(
        max_length=124, unique=True, verbose_name='Modelo')
    branch = models.ForeignKey(
        Branch, on_delete=models.PROTECT, verbose_name='Marca', related_name='models')

    class Meta:
        verbose_name = 'Modelo do equipamento'
        verbose_name_plural = 'Modelos dos equipamentos'
        ordering = ['model']

    def __str__(self):
        return str(f'{self.model} - {self.branch}')


class Category(TimeStampModel):
    category = models.CharField(
        max_length=124, unique=True, verbose_name='Categoria')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['category']

    def __str__(self):
        return self.category


class StatusEquipment(TimeStampModel):
    status = models.CharField(
        max_length=72, unique=True, verbose_name='Status')

    class Meta:
        verbose_name = 'Status do equipamento'
        verbose_name_plural = 'Status dos equipamentos'
        ordering = ['status']

    def __str__(self) -> str:
        return self.status


class Equipment(UserTracking, TimeStampModel):
    branch = models.ForeignKey(
        Branch, on_delete=models.PROTECT, verbose_name='Marca', related_name='equipments')
    model = models.ForeignKey(ModelEquipment, on_delete=models.PROTECT,
                              verbose_name='Modelo', related_name='equipments')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='Categoria', related_name='equipments')
    mac_address = models.CharField(
        max_length=124, verbose_name='Mac Address', unique=True)
    serial_number = models.CharField(
        max_length=124, verbose_name='Serial Number', unique=True)
    status = models.ForeignKey(StatusEquipment, on_delete=models.PROTECT,
                               related_name='equipments', verbose_name='Status')

    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
        ordering = ['model']

    def __str__(self):
        return f'{self.model}'
