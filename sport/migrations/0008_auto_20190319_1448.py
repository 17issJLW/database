# Generated by Django 2.0.8 on 2019-03-19 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0007_auto_20190317_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportmangroup',
            name='grade1',
        ),
        migrations.RemoveField(
            model_name='sportmangroup',
            name='grade2',
        ),
        migrations.RemoveField(
            model_name='sportmangroup',
            name='grade3',
        ),
        migrations.RemoveField(
            model_name='sportmangroup',
            name='grade4',
        ),
        migrations.RemoveField(
            model_name='sportmangroup',
            name='grade5',
        ),
        migrations.AddField(
            model_name='sportman',
            name='number',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='运动员号码'),
        ),
    ]
