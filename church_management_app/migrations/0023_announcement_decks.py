from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0022_remove_notification_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementDeck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('header_text', models.TextField(blank=True, null=True)),
                ('theme_text', models.TextField(blank=True, null=True)),
                ('pptx_file', models.FileField(blank=True, null=True, upload_to='announcement_decks/')),
                ('generated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_announcement_decks', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcement_decks', to='church_management_app.event')),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementDeckItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=1)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='church_management_app.announcementdeck')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]
