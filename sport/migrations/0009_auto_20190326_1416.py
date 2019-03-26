# Generated by Django 2.0.8 on 2019-03-26 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0008_auto_20190319_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='is_pass',
        ),
        migrations.AddField(
            model_name='score',
            name='status',
            field=models.CharField(choices=[('重新打分', '重新打分'), ('待审核', '待审核'), ('已确认', '已确认')], default='待审核', max_length=32, verbose_name='状态'),
        ),
    ]