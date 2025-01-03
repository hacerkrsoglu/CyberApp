# Generated by Django 5.1.2 on 2024-12-02 10:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanner',
            name='url',
            field=models.URLField(max_length=500, unique=True),
        ),
        migrations.AddIndex(
            model_name='scanner',
            index=models.Index(fields=['url'], name='scanner_sca_url_729d6e_idx'),
        ),
        migrations.AddIndex(
            model_name='scanner',
            index=models.Index(fields=['user'], name='scanner_sca_user_id_c608ba_idx'),
        ),
    ]
