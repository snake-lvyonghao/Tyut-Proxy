# Generated by Django 3.0.5 on 2020-04-20 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DoubleHaoapp', '0008_auto_20200415_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='Stype',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]