# Generated by Django 3.2 on 2023-08-27 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0017_alter_division_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SliderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='digitalAssets/frontEnd/images', verbose_name='تصویر اسلایدر')),
                ('Prod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontEnd.product')),
                ('Slider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontEnd.slider')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontEnd.division')),
            ],
        ),
    ]
