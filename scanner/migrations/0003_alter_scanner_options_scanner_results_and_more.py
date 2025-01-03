# Generated by Django 5.1.2 on 2024-12-04 20:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0002_alter_scanner_url_scanner_scanner_sca_url_729d6e_idx_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scanner',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='scanner',
            name='results',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scanner',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scanned_urls', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='scanner',
            index=models.Index(fields=['is_approved'], name='scanner_sca_is_appr_f1e0db_idx'),
        ),
    ]
