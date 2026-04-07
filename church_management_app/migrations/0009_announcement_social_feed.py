from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0008_event_programme_fields_and_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='announcement_images/'),
        ),
        migrations.CreateModel(
            name='AnnouncementLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='church_management_app.announcement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcement_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('announcement', 'user')},
            },
        ),
        migrations.CreateModel(
            name='AnnouncementComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='church_management_app.announcement')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcement_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
