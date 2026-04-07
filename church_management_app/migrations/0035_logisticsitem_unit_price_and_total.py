from decimal import Decimal, InvalidOperation

from django.db import migrations, models


def backfill_logistics_unit_price(apps, schema_editor):
    LogisticsItem = apps.get_model('church_management_app', 'LogisticsItem')
    qs = LogisticsItem.objects.all().only('id', 'quantity', 'purchase_price', 'unit_price')
    for it in qs.iterator():
        if getattr(it, 'unit_price', None) is not None:
            continue
        price = getattr(it, 'purchase_price', None)
        qty = getattr(it, 'quantity', None)
        try:
            qty_int = int(qty or 0)
        except (TypeError, ValueError):
            qty_int = 0
        if price is None or qty_int <= 0:
            continue
        try:
            it.unit_price = (Decimal(str(price)) / Decimal(qty_int)).quantize(Decimal('0.01'))
            it.save(update_fields=['unit_price'])
        except (InvalidOperation, TypeError, ValueError):
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0034_logisticsitem_currency_and_autocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='logisticsitem',
            name='unit_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.RunPython(backfill_logistics_unit_price, migrations.RunPython.noop),
    ]
