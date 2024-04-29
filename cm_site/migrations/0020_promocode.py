# Generated by Django 4.2.5 on 2024-04-26 18:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm_site', '0019_alter_purchasedtrack_track_license'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_create', models.DateTimeField(auto_now_add=True)),
                ('promo_name', models.CharField(max_length=32, unique=True, verbose_name='Name')),
                ('promo_count', models.IntegerField(blank=True, null=True, verbose_name='Amount of use')),
                ('promo_discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Percentage discount (%)')),
            ],
            options={
                'verbose_name': 'Promocode',
                'verbose_name_plural': 'Promocodes',
            },
        ),
    ]