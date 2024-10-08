# Generated by Django 5.1 on 2024-09-01 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.CharField(max_length=10)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.CharField(default='Unknown Customer', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.table'),
        ),
    ]
