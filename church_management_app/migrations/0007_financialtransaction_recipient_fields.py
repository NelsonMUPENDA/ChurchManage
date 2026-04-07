from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0006_financial_document_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialtransaction',
            name='recipient_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='recipient_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='recipient_phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
