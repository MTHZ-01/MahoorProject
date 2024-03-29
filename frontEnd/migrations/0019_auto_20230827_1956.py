# Generated by Django 3.2 on 2023-08-27 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0018_slider_sliderdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sliderdata',
            name='Prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontEnd.product'),
        ),
        migrations.AlterField(
            model_name='sliderdata',
            name='Slider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontEnd.slider'),
        ),
        migrations.AlterField(
            model_name='sliderdata',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontEnd.division'),
        ),
    ]
