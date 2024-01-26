# Generated by Django 3.2 on 2023-08-27 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0024_alter_sliderdata_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='Prod',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontEnd.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slider',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='frontEnd.division'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slider',
            name='img',
            field=models.ImageField(default='', upload_to='digitalAssets/frontEnd/images', verbose_name='تصویر اسلایدر'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SliderData',
        ),
    ]