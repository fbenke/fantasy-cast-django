# Generated by Django 2.0.3 on 2018-06-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=None, max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
