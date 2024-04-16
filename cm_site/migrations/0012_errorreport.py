# Generated by Django 4.2.5 on 2024-04-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm_site', '0011_purchasedtrack'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=256, verbose_name='Subject')),
                ('description', models.TextField(max_length=4096, verbose_name='Description')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/errors/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]