# Generated by Django 5.0.3 on 2024-03-27 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm_core', '0022_apartment_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='lat',
            field=models.CharField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='long',
            field=models.CharField(blank=True, default=0, null=True),
        ),
    ]
