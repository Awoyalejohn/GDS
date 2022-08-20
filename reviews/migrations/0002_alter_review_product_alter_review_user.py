# Generated by Django 4.0.6 on 2022-08-20 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_category_slug_alter_product_category_and_more'),
        ('profiles', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_review', to='products.product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review', to='profiles.userprofile'),
        ),
    ]