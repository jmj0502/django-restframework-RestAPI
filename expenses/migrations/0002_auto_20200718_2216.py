# Generated by Django 3.0.7 on 2020-07-19 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('FOOD', 'FOOD'), ('OTHERS', 'OTHERS'), ('RENT', 'RENT'), ('ONLINE_SERVICES', 'ONLINE_SERVICES'), ('TRAVEL', 'TRAVEL')], max_length=255),
        ),
    ]
