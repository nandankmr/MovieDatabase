# Generated by Django 2.0.5 on 2018-07-03 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20180703_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='certificate',
            field=models.CharField(max_length=20),
        ),
    ]
