# Generated by Django 5.0.3 on 2024-04-01 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='IdealFor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='NeckType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Sleeve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tshirt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500, null=True)),
                ('discount', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='uploads/images')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.brand')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.color')),
                ('ideal_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.idealfor')),
                ('neck_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.necktype')),
                ('occasion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.occasion')),
                ('sleeve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.sleeve')),
            ],
        ),
    ]