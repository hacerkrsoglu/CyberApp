# Generated by Django 5.1.2 on 2024-12-10 10:59

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_message_message_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_image',
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
