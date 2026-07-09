# Сгенерировано Django 6.0.7 2026-07-08 19:51

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlowStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CashFlowType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Тип операции',
                'verbose_name_plural': 'Типы операций',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='cashflows.cashflowtype', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subcategories', to='cashflows.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CashFlowRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.localdate, verbose_name='Дата')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Сумма')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='records', to='cashflows.cashflowstatus', verbose_name='Статус')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='cashflows.cashflowtype', verbose_name='Тип')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='cashflows.category', verbose_name='Категория')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='cashflows.subcategory', verbose_name='Подкатегория')),
            ],
            options={
                'verbose_name': 'Запись ДДС',
                'verbose_name_plural': 'Записи ДДС',
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('type', 'name'), name='unique_category_name_per_type'),
        ),
        migrations.AddConstraint(
            model_name='subcategory',
            constraint=models.UniqueConstraint(fields=('category', 'name'), name='unique_subcategory_name_per_category'),
        ),
    ]
