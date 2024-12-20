# Generated by Django 4.2.16 on 2024-11-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncdc', '0005_disease_donation_weekly_epidemiological_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Situation_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('pdf', models.FileField(upload_to='Situation_reports/')),
            ],
        ),
        migrations.RenameModel(
            old_name='Disease',
            new_name='Report_disease_weekly',
        ),
    ]
