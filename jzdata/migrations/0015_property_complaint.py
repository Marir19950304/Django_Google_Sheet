# Generated by Django 3.2.10 on 2021-12-16 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jzdata', '0014_alter_complaint_bbl'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='complaint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='jzdata.complaint', verbose_name='Complaint'),
        ),
    ]
