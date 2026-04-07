# Generated manually on 2026-03-30

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0037_churchbiography_contact_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Nom complet de l'expéditeur", max_length=150)),
                ('email', models.EmailField(help_text="Email de l'expéditeur", max_length=254)),
                ('phone', models.CharField(blank=True, help_text="Téléphone de l'expéditeur", max_length=30, null=True)),
                ('subject', models.CharField(choices=[('general', 'Demande générale'), ('prayer', 'Demande de prière'), ('visit', 'Planifier une visite'), ('other', 'Autre')], default='general', help_text='Sujet du message', max_length=20)),
                ('message', models.TextField(help_text='Contenu du message')),
                ('status', models.CharField(choices=[('new', 'Nouveau'), ('read', 'Lu'), ('in_progress', 'En cours'), ('answered', 'Répondu'), ('archived', 'Archivé')], default='new', help_text='Statut du message', max_length=20)),
                ('notes', models.TextField(blank=True, help_text='Notes internes pour l\'administration', null=True)),
                ('answered_at', models.DateTimeField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text="Adresse IP de l'expéditeur", null=True)),
                ('user_agent', models.TextField(blank=True, help_text='User agent du navigateur', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answered_contacts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message de contact',
                'verbose_name_plural': 'Messages de contact',
                'ordering': ['-created_at'],
            },
        ),
    ]
