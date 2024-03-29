# Generated by Django 4.0.6 on 2022-08-13 13:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('type', models.CharField(choices=[('IC', 'Icon'), ('LG', 'Logo'), ('PS', 'Poster'), ('ST', 'Sticker'), ('WP', 'Wallpaper'), ('BN', 'Banner')], max_length=2)),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=1)),
                ('description', models.TextField()),
                ('submitted', models.DateTimeField(auto_now_add=True)),
                ('quote_order_number', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.userprofile')),
            ],
        ),
    ]
