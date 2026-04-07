from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0035_logisticsitem_unit_price_and_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='evangelismactivity',
            name='custom_activity_type',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='evangelismactivity',
            name='activity_type',
            field=models.CharField(
                choices=[('field', 'Descente sur terrain'), ('prayer', 'Réunion de prière'), ('other', 'Autre')],
                default='field',
                max_length=20,
            ),
        ),
    ]
