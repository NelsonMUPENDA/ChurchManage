from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0017_evangelisation_and_marriage'),
    ]

    operations = [
        migrations.AddField(
            model_name='marriagerecord',
            name='groom_full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='marriagerecord',
            name='bride_full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='marriagerecord',
            name='groom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='marriages_as_groom', to='church_management_app.member'),
        ),
        migrations.AlterField(
            model_name='marriagerecord',
            name='bride',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='marriages_as_bride', to='church_management_app.member'),
        ),
    ]
