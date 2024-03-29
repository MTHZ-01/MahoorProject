# Generated by Django 4.2.5 on 2024-01-27 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0030_product_productcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsinorder',
            name='chainPosition',
            field=models.CharField(max_length=1000, null=True, verbose_name='محل زنجیر'),
        ),
        migrations.AlterField(
            model_name='productsinorder',
            name='explainations',
            field=models.CharField(max_length=1000, null=True, verbose_name='توضیحات مشتری درباره این مورد'),
        ),
        migrations.AlterField(
            model_name='productsinorder',
            name='height',
            field=models.IntegerField(verbose_name='ارتفاع'),
        ),
        migrations.AlterField(
            model_name='productsinorder',
            name='installationPosition',
            field=models.CharField(max_length=1000, null=True, verbose_name='محل نصب'),
        ),
        migrations.AlterField(
            model_name='productsinorder',
            name='prod',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='frontEnd.product', verbose_name='نام محصول'),
        ),
        migrations.AlterField(
            model_name='productsinorder',
            name='width',
            field=models.IntegerField(verbose_name='طول'),
        ),
    ]
