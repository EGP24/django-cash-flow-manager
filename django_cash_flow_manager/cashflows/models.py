from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from django_cash_flow_manager.cashflows.rules import validate_transaction_dependencies


class NamedCatalogModel(models.Model):
    """Базовая абстрактная модель именованного справочника."""

    name = models.CharField('Название', max_length=120, unique=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


class CashFlowStatus(NamedCatalogModel):
    """Статус записи движения денежных средств."""

    class Meta:
        ordering = ['name']
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class CashFlowType(NamedCatalogModel):
    """Тип операции движения денежных средств."""

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'


class Category(models.Model):
    """Категория операции, привязанная к конкретному типу ДДС."""

    name = models.CharField('Название', max_length=120)
    type = models.ForeignKey(CashFlowType, verbose_name='Тип', on_delete=models.PROTECT, related_name='categories')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(fields=['type', 'name'], name='unique_category_name_per_type'),
        ]

    def __str__(self) -> str:
        return f'{self.type}: {self.name}'


class Subcategory(models.Model):
    """Подкатегория операции, привязанная к конкретной категории."""

    name = models.CharField('Название', max_length=120)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='subcategories',
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        constraints = [
            models.UniqueConstraint(fields=['category', 'name'], name='unique_subcategory_name_per_category'),
        ]

    def __str__(self) -> str:
        return f'{self.category.name}: {self.name}'


class CashFlowTransaction(models.Model):
    """Запись движения денежных средств."""

    date = models.DateField('Дата', default=timezone.localdate)
    status = models.ForeignKey(
        CashFlowStatus,
        verbose_name='Статус',
        on_delete=models.PROTECT,
        related_name='transactions',
        blank=True,
        null=True,
    )
    type = models.ForeignKey(CashFlowType, verbose_name='Тип', on_delete=models.PROTECT, related_name='transactions')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        verbose_name='Подкатегория',
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Запись ДДС'
        verbose_name_plural = 'Записи ДДС'

    def __str__(self) -> str:
        return f'{self.date}: {self.type} {self.amount}'

    def clean(self) -> None:
        validate_transaction_dependencies(
            type_id=self.type_id,
            category_id=self.category_id,
            category_type_id=self.category.type_id if self.category_id else None,
            subcategory_category_id=self.subcategory.category_id if self.subcategory_id else None,
        )
