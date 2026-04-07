from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0012_logistics_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='church_management_app.department'),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='financial_transactions', to='church_management_app.event'),
        ),
        migrations.CreateModel(
            name='EventAttendanceAggregate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('male_adults', models.PositiveIntegerField(default=0)),
                ('female_adults', models.PositiveIntegerField(default=0)),
                ('male_children', models.PositiveIntegerField(default=0)),
                ('female_children', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_aggregate', to='church_management_app.event')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_event_attendance_aggregates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
