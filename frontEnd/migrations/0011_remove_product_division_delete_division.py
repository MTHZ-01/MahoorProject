# Generated by Django 4.2.4 on 2023-08-24 09:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("frontEnd", "0010_division_product_division"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="division",
        ),
        migrations.DeleteModel(
            name="division",
        ),
    ]
