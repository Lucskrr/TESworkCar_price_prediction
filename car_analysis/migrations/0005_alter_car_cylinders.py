# Generated by Django 5.1.3 on 2024-11-29 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_analysis", "0004_alter_car_mileage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="cylinders",
            field=models.FloatField(blank=True, null=True),
        ),
    ]