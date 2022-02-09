# Generated by Django 3.2.9 on 2022-02-06 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='project',
            field=models.CharField(blank=True, choices=[(0, 'CheckMyMetal'), (1, 'Other')], default=0, help_text='Project to which the bug is reported', max_length=1),
        ),
        migrations.AlterField(
            model_name='bug',
            name='status',
            field=models.CharField(default='Not fixed', help_text='Select a status for this bug', max_length=20),
        ),
    ]