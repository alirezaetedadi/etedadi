# Generated by Django 2.0.4 on 2018-11-30 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_customer_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digits',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
