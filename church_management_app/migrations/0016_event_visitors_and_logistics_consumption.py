from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0015_event_closure_alert_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventVisitorAggregate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('male_visitors', models.PositiveIntegerField(default=0)),
                ('female_visitors', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='visitor_aggregate', to='church_management_app.event')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_event_visitor_aggregates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventLogisticsConsumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_used', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logistics_consumptions', to='church_management_app.event')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_consumptions', to='church_management_app.logisticsitem')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_event_logistics_consumptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('event', 'item')},
            },
        ),
    ]
