# Generated by Django 4.0.6 on 2022-07-24 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_category_friendly_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
