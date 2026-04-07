from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0023_announcement_decks'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=10)),
                ('target_object_id', models.CharField(blank=True, max_length=64, null=True)),
                ('object_repr', models.CharField(blank=True, max_length=200, null=True)),
                ('payload', models.JSONField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('decided_at', models.DateTimeField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('decided_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='decided_approval_requests', to=settings.AUTH_USER_MODEL)),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
