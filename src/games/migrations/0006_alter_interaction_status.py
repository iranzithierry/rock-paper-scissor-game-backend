# Generated by Django 3.2.12 on 2024-05-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20240524_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='status',
            field=models.CharField(default='disconnected', max_length=40),
        ),
    ]
