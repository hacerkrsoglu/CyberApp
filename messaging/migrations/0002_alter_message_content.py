# Generated by Django 5.1.2 on 2024-12-02 12:14

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
