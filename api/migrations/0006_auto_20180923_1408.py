# Generated by Django 2.0.4 on 2018-09-23 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_product_inviter_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='digits',
            field=models.CharField(max_length=13, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='inviter',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.customer'),
        ),
    ]
