# Generated by Django 3.2.10 on 2021-12-11 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_alter_property_extracrdt'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_id', models.CharField(max_length=64, verbose_name='Document Id')),
                ('boro', models.CharField(blank=True, max_length=64, null=True, verbose_name='BORO')),
                ('block', models.CharField(blank=True, max_length=64, null=True, verbose_name='BLOCK')),
                ('lot', models.CharField(blank=True, max_length=64, null=True, verbose_name='LOT')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name': 'property assessment', 'verbose_name_plural': 'property assessments'},
        ),
        migrations.AddField(
            model_name='property',
            name='step',
            field=models.IntegerField(default=0, verbose_name='Step'),
        ),
    ]
