# Generated by Django 5.0.3 on 2024-04-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0013_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='tshirt',
            name='slug',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
