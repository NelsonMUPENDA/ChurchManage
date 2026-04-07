from django.db import migrations, models


def backfill_logistics_asset_tags(apps, schema_editor):
    LogisticsItem = apps.get_model('church_management_app', 'LogisticsItem')
    qs = LogisticsItem.objects.filter(asset_tag__isnull=True).only('id', 'asset_tag')
    for it in qs.iterator():
        if not getattr(it, 'asset_tag', None) and getattr(it, 'id', None):
            it.asset_tag = f"CPD-LOG-{it.id:06d}"
            it.save(update_fields=['asset_tag'])


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0033_activityduration_and_event_duration_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='logisticsitem',
            name='purchase_currency',
            field=models.CharField(choices=[('CDF', 'CDF'), ('USD', 'USD')], default='CDF', max_length=3),
        ),
        migrations.RunPython(backfill_logistics_asset_tags, migrations.RunPython.noop),
    ]
