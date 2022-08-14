# Generated by Django 4.1 on 2022-08-12 21:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="number",
            field=models.PositiveIntegerField(
                db_index=True, verbose_name="заказ №"
            ),
        ),
        migrations.AlterField(
            model_name="rubleprice",
            name="exchange_date",
            field=models.DateField(
                default=datetime.date.today, verbose_name="Exchange Date"
            ),
        ),
    ]
