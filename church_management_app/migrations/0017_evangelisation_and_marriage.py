from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0016_event_visitors_and_logistics_consumption'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaptismEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_baptism_events', to=settings.AUTH_USER_MODEL)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='baptism_event', to='church_management_app.event')),
            ],
        ),
        migrations.CreateModel(
            name='EvangelismActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('activity_type', models.CharField(choices=[('field', 'Descente sur terrain'), ('prayer', 'Réunion de prière')], default='field', max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_evangelism_activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=200)),
                ('trainer', models.CharField(max_length=150)),
                ('lesson', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_training_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarriageRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planned_date', models.DateField()),
                ('planned_time', models.TimeField()),
                ('location', models.CharField(max_length=200)),
                ('dowry_paid', models.BooleanField(default=False)),
                ('civil_verified', models.BooleanField(default=False)),
                ('prenuptial_tests', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bride', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='marriages_as_bride', to='church_management_app.member')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_marriage_records', to=settings.AUTH_USER_MODEL)),
                ('groom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='marriages_as_groom', to='church_management_app.member')),
                ('published_event', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriage_record', to='church_management_app.event')),
            ],
        ),
        migrations.CreateModel(
            name='BaptismCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('post_name', models.CharField(max_length=120)),
                ('place_of_birth', models.CharField(max_length=150)),
                ('birth_date', models.DateField()),
                ('passport_photo', models.ImageField(blank=True, null=True, upload_to='baptism_photos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('baptism_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='church_management_app.baptismevent')),
            ],
        ),
    ]
