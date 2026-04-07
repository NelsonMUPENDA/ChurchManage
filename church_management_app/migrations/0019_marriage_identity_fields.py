from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0018_marriage_manual_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='marriagerecord',
            name='groom_birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='groom_birth_place',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='groom_nationality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='groom_passport_photo',
            field=models.ImageField(blank=True, null=True, upload_to='marriage_photos/'),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='bride_birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='bride_birth_place',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='bride_nationality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='bride_passport_photo',
            field=models.ImageField(blank=True, null=True, upload_to='marriage_photos/'),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='godfather_full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='godfather_nationality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='godfather_passport_photo',
            field=models.ImageField(blank=True, null=True, upload_to='marriage_photos/'),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='godmother_full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='godmother_nationality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='godmother_passport_photo',
            field=models.ImageField(blank=True, null=True, upload_to='marriage_photos/'),
        ),
    ]
