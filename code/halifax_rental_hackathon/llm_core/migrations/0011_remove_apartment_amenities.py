# Generated by Django 5.0.3 on 2024-03-25 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('llm_core', '0010_delete_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='amenities',
        ),
    ]