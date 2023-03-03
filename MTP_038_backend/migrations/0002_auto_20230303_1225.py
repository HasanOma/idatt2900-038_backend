# Generated by Django 3.2.16 on 2023-03-03 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MTP_038_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordinate',
            name='east',
            field=models.DecimalField(decimal_places=8, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='coordinate',
            name='north',
            field=models.DecimalField(decimal_places=8, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='coordinate',
            name='south',
            field=models.DecimalField(decimal_places=8, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='coordinate',
            name='west',
            field=models.DecimalField(decimal_places=8, max_digits=14, null=True),
        ),
    ]
