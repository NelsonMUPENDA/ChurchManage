from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0013_event_attendance_aggregate_and_finance_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('report_type', models.CharField(choices=[('activity', 'Activity Report'), ('compiled', 'Compiled Report'), ('programme', 'Programme PDF')], max_length=20)),
                ('payload', models.JSONField(blank=True, null=True)),
                ('pdf_sha256', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_certificates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
