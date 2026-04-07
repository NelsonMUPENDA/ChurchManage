from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0020_financialtransaction_types_and_evangelisation_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='baptismevent',
            name='executors',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='evangelismactivity',
            name='moderator',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
