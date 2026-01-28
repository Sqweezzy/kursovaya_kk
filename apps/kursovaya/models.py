# Определяет модель kursovaya для работы с БД
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


class Location(models.Model):
    """Модель местоположения оборудования"""
    zone_name = models.CharField(
        max_length=50,
        verbose_name='Зона',
        help_text='Введите название зоны'
    )
    workstation_number = models.CharField(
        max_length=10,
        verbose_name='Номер игрового места',
        help_text='Введите номер игрового места'
    )
    description = models.TextField(
        validators=[MaxLengthValidator(10000)],
        verbose_name='Описание местоположения',
        help_text='Добавьте описание для места',
        blank=True,
    )
    
    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ['zone_name', 'workstation_number']
    
    def __str__(self):
        return f"{self.zone_name} - {self.workstation_number}"


class EquipmentType(models.Model):
    """Тип оборудования"""
    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    type_name = models.CharField(
        max_length=50,
        verbose_name='Тип оборудования',
        help_text='Введите тип оборудования',
    )
    category = models.CharField(
        max_length=50,
        verbose_name='Категория',
        help_text='Введите категорию оборудования',
    )
    description = models.TextField(
        verbose_name='Описание оборудования',
        help_text='Добавьте описание оборудования',
        blank=True,
    )
    
    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'
        ordering = ['category', 'type_name']
    
    def __str__(self):
        return f"{self.category} - {self.type_name}"


class EquipmentStatus(models.Model):
    """Статус оборудования"""
    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    status_name = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Активно'),
            ('inactive', 'Неактивно'),
            ('maintenance', 'На обслуживании'),
        ],
        verbose_name='Статус',
        help_text='Выберите статус оборудования'
    )
    description = models.TextField(
        validators=[MaxLengthValidator(10000)],
        verbose_name='Описание',
        help_text='Добавьте описание',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Статус оборудования'
        verbose_name_plural = 'Статусы оборудования'
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.equipment} {self.status_name}'
    
class Specification(models.Model):
    """Данные оборудования"""
    spec_name = models.CharField(
        max_length=50,
        verbose_name='Название характеристики',
        help_text='Введите название характеристики'
    )
    spec_value = models.CharField(
        max_length=50,
        verbose_name='Значение',
        help_text='Введите значение характеристики'
    )
    unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
    )
    
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['spec_name']
    
    def __str__(self):
        return f'{self.spec_name} {self.spec_value}{self.unit}'

class Equipment(models.Model):
    """Оборудование"""
    inventory_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Инвентарный номер',
        help_text='Введите инвентарный номер'
    )
    name = models.CharField(
        max_length=75,
        verbose_name='Название',
        help_text='Введите название оборудования'
    )
    manufacturer = models.CharField(
        max_length=75,
        verbose_name='Производитель',
        help_text='Введите производителя'
    )
    model = models.CharField(
        max_length=75,
        verbose_name='Модель',
        help_text='Введите модель оборудования'
    )
    serial_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Серийный номер',
        help_text='Введите серийный номер'
    )
    current_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Текущее местоположение',
        help_text='Выберите текущее местоположение'
    )
    warranty_expiry_date = models.DateField(
        verbose_name='Дата окончания гарантии',
        help_text='Введите дату окончания гарантии',
        null=True,
        blank=True
    )
    notes = models.TextField(
        validators=[MaxLengthValidator(10000)],
        verbose_name='Примечания',
        help_text='Введите примечания',
        blank=True
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name[:50]
    
class EquipmentSpecification(models.Model):
    """Вспомогательная таблица"""
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        verbose_name='Характеристика'
    )
    
    class Meta:
        verbose_name = 'Характеристика оборудования'
        verbose_name_plural = 'Характеристики оборудования'


class Movement(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    from_location = models.ForeignKey(
        Location,
        related_name='movements_from',
        on_delete=models.CASCADE,
        verbose_name='Откуда',
        help_text='Выберите исходное местоположение'
    )
    to_location = models.ForeignKey(
        Location,
        related_name='movements_to',
        on_delete=models.CASCADE,
        verbose_name='Куда',
        help_text='Выберите новое местоположение'
    )
    movement_date = models.DateField(
        verbose_name='Дата перемещения',
        help_text='Введите дату перемещения'
    )
    reason = models.TextField(
        validators=[MaxLengthValidator(10000)],
        verbose_name='Причина',
        help_text='Введите причину перемещения'
    )
    responsible_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Ответственный',
        help_text='Выберите ответственного пользователя'
    )
    
    class Meta:
        verbose_name = 'Перемещение'
        verbose_name_plural = 'Перемещения'
        ordering = ['-movement_date']


class WriteOff(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    write_off_date = models.DateField(
        verbose_name='Дата списания',
        help_text='Введите дату списания'
    )
    reason = models.TextField(
        validators=[MaxLengthValidator(10000)],
        verbose_name='Причина',
        help_text='Введите причину списания'
    )
    act_number = models.IntegerField(
        unique=True,
        verbose_name='Номер акта',
        help_text='Введите номер акта списания'
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Утвердил',
        help_text='Выберите утвердившего пользователя'
    )
    notes = models.TextField(
        validators=[MaxLengthValidator(10000)],
        verbose_name='Примечания',
        help_text='Введите примечания к списанию',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Списание'
        verbose_name_plural = 'Списания'
        ordering = ['-write_off_date']