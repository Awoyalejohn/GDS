# Generated by Django 4.0.6 on 2022-08-14 19:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_remove_quoterequest_quote_request_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterequest',
            name='quote_request_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='quoteorder',
            name='quote_order_number',
            field=models.CharField(max_length=250),
        ),
    ]
