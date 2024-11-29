# Generated by Django 5.1.3 on 2024-11-29 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_analysis", "0002_alter_car_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="engine_volume",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="car",
            name="leather_interior",
            field=models.BooleanField(default=False),
        ),
    ]