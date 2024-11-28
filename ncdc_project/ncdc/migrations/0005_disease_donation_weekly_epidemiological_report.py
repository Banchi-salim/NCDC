# Generated by Django 4.2.16 on 2024-11-25 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncdc', '0004_diseasealert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('points', models.TextField(help_text='Key points about the disease')),
                ('image', models.ImageField(blank=True, null=True, upload_to='disease_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weekly_Epidemiological_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('month', models.CharField(max_length=20)),
                ('week', models.PositiveIntegerField()),
                ('summary', models.TextField()),
                ('diseases', models.ManyToManyField(related_name='reports', to='ncdc.disease')),
            ],
        ),
    ]