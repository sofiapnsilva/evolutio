# Generated by Django 5.0.1 on 2024-01-25 00:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evolutioapi', '0002_alter_delivery_id_alter_delivery_shipped_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='reference',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='DeliveryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evolutioapi.delivery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evolutioapi.product')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='products',
            field=models.ManyToManyField(through='evolutioapi.DeliveryProduct', to='evolutioapi.product'),
        ),
    ]
