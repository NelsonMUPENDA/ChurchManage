from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0009_announcement_social_feed'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementCommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='church_management_app.announcementcomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcement_comment_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('comment', 'user')},
            },
        ),
    ]
