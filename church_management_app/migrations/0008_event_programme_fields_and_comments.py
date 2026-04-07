from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0007_financialtransaction_recipient_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration_type',
            field=models.CharField(choices=[('daily', 'Journalière'), ('weekly', 'Hebdomadaire'), ('21d', '21 jours'), ('40d', '40 jours')], default='daily', max_length=10),
        ),
        migrations.AddField(
            model_name='event',
            name='moderator',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='preacher',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='choir',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='protocol_team',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='tech_team',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='communicator',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='poster_image',
            field=models.ImageField(blank=True, null=True, upload_to='event_posters/'),
        ),
        migrations.AddField(
            model_name='event',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='share_slug',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='EventComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(blank=True, max_length=150, null=True)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='church_management_app.event')),
            ],
        ),
    ]
