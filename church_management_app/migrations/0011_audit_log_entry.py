from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0010_announcement_comment_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=10)),
                ('model', models.CharField(max_length=100)),
                ('object_id', models.CharField(max_length=64)),
                ('object_repr', models.CharField(blank=True, max_length=200, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('payload', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
