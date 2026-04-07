from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0003_member_identity_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialtransaction',
            name='donor_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='donor_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='payment_method',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='reference_number',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='cashier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cashier_transactions', to='church_management_app.user'),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_transactions', to='church_management_app.user'),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='receipt_code',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='receipt_pdf',
            field=models.FileField(blank=True, null=True, upload_to='receipts/'),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='receipt_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='proof_image',
            field=models.ImageField(blank=True, null=True, upload_to='expense_proofs/'),
        ),
    ]
