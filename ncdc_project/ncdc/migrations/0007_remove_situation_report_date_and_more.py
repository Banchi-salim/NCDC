# Generated by Django 4.2.16 on 2024-11-26 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ncdc', '0006_situation_report_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situation_report',
            name='date',
        ),
        migrations.RemoveField(
            model_name='situation_report',
            name='pdf',
        ),
    ]
