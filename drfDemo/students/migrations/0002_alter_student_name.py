# Generated by Django 3.2.12 on 2022-02-23 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=32, verbose_name='姓名'),
        ),
    ]
