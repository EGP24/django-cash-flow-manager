import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cashflows', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CashFlowRecord',
            new_name='CashFlowTransaction',
        ),
        migrations.AlterField(
            model_name='cashflowtransaction',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transactions',
                to='cashflows.category',
                verbose_name='Категория',
            ),
        ),
        migrations.AlterField(
            model_name='cashflowtransaction',
            name='status',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transactions',
                to='cashflows.cashflowstatus',
                verbose_name='Статус',
            ),
        ),
        migrations.AlterField(
            model_name='cashflowtransaction',
            name='subcategory',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transactions',
                to='cashflows.subcategory',
                verbose_name='Подкатегория',
            ),
        ),
        migrations.AlterField(
            model_name='cashflowtransaction',
            name='type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='transactions',
                to='cashflows.cashflowtype',
                verbose_name='Тип',
            ),
        ),
    ]
