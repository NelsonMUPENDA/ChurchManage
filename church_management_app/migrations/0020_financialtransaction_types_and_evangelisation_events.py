from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


def forwards_create_linked_events(apps, schema_editor):
    Event = apps.get_model('church_management_app', 'Event')
    EvangelismActivity = apps.get_model('church_management_app', 'EvangelismActivity')
    TrainingEvent = apps.get_model('church_management_app', 'TrainingEvent')

    now = timezone.now()

    for row in EvangelismActivity.objects.filter(published_event__isnull=True).order_by('id'):
        ev = Event.objects.create(
            title=(getattr(row, 'title', None) or 'Évangélisation')[:200],
            date=getattr(row, 'date', None),
            time=getattr(row, 'time', None),
            location=getattr(row, 'location', None),
            event_type='evangelism',
            duration_type='daily',
            is_published=True,
            published_at=now,
        )
        row.published_event_id = ev.id
        row.save(update_fields=['published_event'])

    for row in TrainingEvent.objects.filter(published_event__isnull=True).order_by('id'):
        ev = Event.objects.create(
            title=(getattr(row, 'title', None) or 'Affermissement')[:200],
            date=getattr(row, 'date', None),
            time=getattr(row, 'time', None),
            location=getattr(row, 'location', None),
            event_type='training',
            duration_type='daily',
            is_published=True,
            published_at=now,
        )
        row.published_event_id = ev.id
        row.save(update_fields=['published_event'])


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0019_marriage_identity_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='evangelismactivity',
            name='published_event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evangelism_activity', to='church_management_app.event'),
        ),
        migrations.AddField(
            model_name='trainingevent',
            name='published_event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='training_event', to='church_management_app.event'),
        ),
        migrations.AlterField(
            model_name='financialtransaction',
            name='transaction_type',
            field=models.CharField(choices=[('offering', 'Offrandes'), ('tithe', 'Dîmes'), ('thanksgiving', 'Actions de grâce'), ('construction', 'Construction'), ('project_fund', 'Fonds projet'), ('special_donation', 'Don spécial'), ('donation', 'Don'), ('seed_vow', 'Semences et Vœux'), ('gift_other', 'Dons et autres'), ('functioning', 'Fonctionnement'), ('transport_communication', 'Transport et communication'), ('investment', 'Investissement'), ('rehabilitation', 'Réhabilitation'), ('social_assistance', 'Assistance Sociale')], default='offering', max_length=50),
        ),
        migrations.RunPython(forwards_create_linked_events, migrations.RunPython.noop),
    ]
