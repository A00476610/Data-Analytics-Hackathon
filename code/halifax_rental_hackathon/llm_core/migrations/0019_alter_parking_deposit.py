# Generated by Django 5.0.3 on 2024-03-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm_core', '0018_parking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='deposit',
            field=models.CharField(blank=True, default=0, null=True),
        ),
    ]