# Generated by Django 2.2.6 on 2019-10-22 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexpromotionbanner',
            name='url',
            field=models.CharField(max_length=256, verbose_name='活动链接'),
        ),
    ]
