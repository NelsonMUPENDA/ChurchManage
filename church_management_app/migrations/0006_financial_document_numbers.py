from django.db import migrations, models


def forwards(apps, schema_editor):
    FinancialTransaction = apps.get_model('church_management_app', 'FinancialTransaction')
    FinancialDocumentSequence = apps.get_model('church_management_app', 'FinancialDocumentSequence')

    for tx in FinancialTransaction.objects.all().order_by('date', 'id'):
        if tx.document_number:
            continue

        year = tx.date.year if tx.date else 0
        prefix = 'RC' if tx.direction == 'in' else 'BS'

        seq, _ = FinancialDocumentSequence.objects.get_or_create(prefix=prefix, year=year, defaults={'last_number': 0})
        seq.last_number = (seq.last_number or 0) + 1
        seq.save(update_fields=['last_number'])

        tx.document_number = f"{prefix}-{year}-{seq.last_number:06d}"
        update_fields = ['document_number']
        if tx.direction == 'in' and not tx.receipt_code:
            tx.receipt_code = tx.document_number
            update_fields.append('receipt_code')
        tx.save(update_fields=update_fields)


def backwards(apps, schema_editor):
    FinancialTransaction = apps.get_model('church_management_app', 'FinancialTransaction')
    FinancialDocumentSequence = apps.get_model('church_management_app', 'FinancialDocumentSequence')

    FinancialTransaction.objects.all().update(document_number=None)
    FinancialDocumentSequence.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0005_create_default_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialDocumentSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=4)),
                ('year', models.PositiveIntegerField()),
                ('last_number', models.PositiveIntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('prefix', 'year')},
            },
        ),
        migrations.AddField(
            model_name='financialtransaction',
            name='document_number',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
        migrations.RunPython(forwards, backwards),
    ]
