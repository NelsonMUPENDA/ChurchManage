from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_management_app', '0011_audit_log_entry'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogisticsItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('asset_tag', models.CharField(blank=True, max_length=60, null=True, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('unit', models.CharField(blank=True, max_length=30, null=True)),
                (
                    'condition',
                    models.CharField(
                        choices=[
                            ('new', 'New'),
                            ('good', 'Good'),
                            ('fair', 'Fair'),
                            ('needs_repair', 'Needs Repair'),
                            ('damaged', 'Damaged'),
                        ],
                        default='good',
                        max_length=20,
                    ),
                ),
                ('location', models.CharField(blank=True, max_length=120, null=True)),
                ('acquired_date', models.DateField(blank=True, null=True)),
                ('purchase_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('supplier', models.CharField(blank=True, max_length=150, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
