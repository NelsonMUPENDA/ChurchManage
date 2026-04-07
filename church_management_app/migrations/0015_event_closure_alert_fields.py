from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0014_report_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='closure_validated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='is_alert',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='alert_message',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
