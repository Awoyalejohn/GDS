# Generated by Django 4.0.6 on 2022-08-19 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0010_quotefufillment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotefufillment',
            name='quote_order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_order_set', to='quotes.quoteorder'),
        ),
    ]
