# Generated by Django 3.1.3 on 2023-08-26 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election_app', '0003_auto_20230826_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='election',
            name='closing_datetime',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='is_checked',
        ),
        migrations.AlterField(
            model_name='election',
            name='is_voting_open',
            field=models.BooleanField(default=True),
        ),
    ]
