# Generated by Django 4.2.4 on 2023-08-23 20:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("frontEnd", "0008_alter_fetures_options_alter_specs_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fetures",
            options={
                "verbose_name": "ویژگی",
                "verbose_name_plural": "بخش ویژگی ها در صفحه محصول",
            },
        ),
        migrations.AlterModelOptions(
            name="specs",
            options={
                "verbose_name": "مشخصه",
                "verbose_name_plural": "بخش مشخصات در صفحه محصول",
            },
        ),
    ]
