from django.db import migrations, models


def seed_activity_durations(apps, schema_editor):
    ActivityDuration = apps.get_model('church_management_app', 'ActivityDuration')
    defaults = [
        ('daily', 'Journalière', 10),
        ('weekly', 'Hebdomadaire', 20),
        ('21d', '21 jours', 30),
        ('40d', '40 jours', 40),
    ]
    for code, label, order in defaults:
        ActivityDuration.objects.get_or_create(
            code=code,
            defaults={'label': label, 'sort_order': order, 'is_active': True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0032_member_public_function_church_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityDuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('label', models.CharField(max_length=60)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='duration_type',
            field=models.CharField(default='daily', max_length=20),
        ),
        migrations.RunPython(seed_activity_durations, migrations.RunPython.noop),
    ]
