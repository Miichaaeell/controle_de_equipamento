from django.db import models
from controllers.models import TimeStampModel, UserTracking


class Brand(TimeStampModel):
    brand = models.CharField(
        max_length=124, unique=True, verbose_name='Marca')

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['brand']

    def save(self, *args, **kwargs):
        if self.brand:
            self.brand = self.brand.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.brand


class ModelEquipment(TimeStampModel):
    model = models.CharField(
        max_length=124, verbose_name='Modelo')
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, verbose_name='Marca', related_name='models')

    class Meta:
        verbose_name = 'Modelo do equipamento'
        verbose_name_plural = 'Modelos dos equipamentos'
        ordering = ['model']
        unique_together = ['model', 'brand']

    def save(self, *args, **kwargs):
        if self.model:
            self.model = self.model.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f'{self.model}')


class Category(TimeStampModel):
    category = models.CharField(
        max_length=124, unique=True, verbose_name='Categoria')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['category']

    def save(self, *args, **kwargs):
        if self.category:
            self.category = self.category.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category


class StatusEquipment(TimeStampModel):
    status = models.CharField(
        max_length=72, unique=True, verbose_name='Status')

    class Meta:
        verbose_name = 'Status do equipamento'
        verbose_name_plural = 'Status dos equipamentos'
        ordering = ['status']

    def save(self, *args, **kwargs):
        if self.status:
            self.status = self.status.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.status


class Equipment(UserTracking, TimeStampModel):
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, verbose_name='Marca', related_name='equipments')
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

    def save(self, *args, **kwargs):
        if self.mac_address and self.serial_number:
            self.mac_address = self.mac_address.upper()
            self.serial_number = self.serial_number.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.model}'
