# Generated by Django 3.2.10 on 2021-12-16 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0015_property_complaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='extracrdt',
            field=models.CharField(default='test', max_length=64, verbose_name='EXTRACRDT'),
            preserve_default=False,
        ),
    ]