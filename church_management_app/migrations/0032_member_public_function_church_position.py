from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0031_member_inactive_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='public_function',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='church_position',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
