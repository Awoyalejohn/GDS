# Generated by Django 4.0.6 on 2022-08-14 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0007_quoterequest_quote_request_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quoteorder',
            name='quote_order_number',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_number',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]