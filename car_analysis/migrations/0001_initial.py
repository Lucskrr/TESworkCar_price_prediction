# Generated by Django 5.1.1 on 2024-11-28 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("price", models.IntegerField()),
                ("levy", models.CharField(blank=True, max_length=100, null=True)),
                ("manufacturer", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("prod_year", models.IntegerField()),
                ("category", models.CharField(max_length=100)),
                ("leather_interior", models.BooleanField()),
                ("fuel_type", models.CharField(max_length=50)),
                ("engine_volume", models.FloatField()),
                ("mileage", models.IntegerField()),
                ("cylinders", models.FloatField()),
                ("gear_box_type", models.CharField(max_length=50)),
                ("drive_wheels", models.CharField(max_length=50)),
                ("doors", models.IntegerField()),
                ("wheel", models.CharField(max_length=50)),
                ("color", models.CharField(max_length=50)),
                ("airbags", models.IntegerField()),
            ],
        ),
    ]