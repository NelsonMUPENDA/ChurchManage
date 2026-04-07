from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0025_member_user_set_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='post_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
