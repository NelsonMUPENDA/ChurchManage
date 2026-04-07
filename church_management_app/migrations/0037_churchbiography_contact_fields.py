# Generated manually on 2026-03-30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0036_evangelismactivity_custom_activity_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchbiography',
            name='address',
            field=models.TextField(blank=True, null=True, help_text="Adresse complète de l'église"),
        ),
        migrations.AddField(
            model_name='churchbiography',
            name='phone',
            field=models.CharField(max_length=50, blank=True, null=True, help_text="Numéro de téléphone principal"),
        ),
        migrations.AddField(
            model_name='churchbiography',
            name='email',
            field=models.EmailField(max_length=254, blank=True, null=True, help_text="Email de contact"),
        ),
        migrations.AddField(
            model_name='churchbiography',
            name='facebook_url',
            field=models.URLField(blank=True, null=True, help_text="Lien Facebook"),
        ),
        migrations.AddField(
            model_name='churchbiography',
            name='youtube_url',
            field=models.URLField(blank=True, null=True, help_text="Lien YouTube"),
        ),
        migrations.AddField(
            model_name='churchbiography',
            name='instagram_url',
            field=models.URLField(blank=True, null=True, help_text="Lien Instagram"),
        ),
        migrations.AddField(
            model_name='churchbiography',
            name='service_times',
            field=models.JSONField(blank=True, null=True, default=list, help_text="Horaires des cultes (JSON)"),
        ),
    ]
