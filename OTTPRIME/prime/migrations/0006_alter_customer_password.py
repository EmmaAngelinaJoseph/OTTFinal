# Generated by Django 5.0.6 on 2024-05-30 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prime', '0005_movies_disabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
