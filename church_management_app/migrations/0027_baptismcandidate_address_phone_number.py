from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0026_member_post_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='baptismcandidate',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='baptismcandidate',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
