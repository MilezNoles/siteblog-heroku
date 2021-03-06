# Generated by Django 3.1.7 on 2021-05-03 15:31

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobscrapper', '0006_auto_20210430_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Errors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Ошибка',
                'verbose_name_plural': 'Ошибки',
                'ordering': ['-timestamp'],
            },
        ),
    ]
