# Generated by Django 3.2.6 on 2021-08-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vtrees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='videos_lastupdate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]