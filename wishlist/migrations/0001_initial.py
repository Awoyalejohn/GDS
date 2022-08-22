# Generated by Django 4.0.6 on 2022-08-22 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0003_rename_first_last_userprofile_last_name'),
        ('products', '0008_alter_category_slug_alter_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list_item', to='products.product')),
                ('wish_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list_item', to='wishlist.wishlist')),
            ],
            options={
                'unique_together': {('wish_list', 'product')},
            },
        ),
    ]
