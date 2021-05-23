# Generated by Django 3.2.3 on 2021-05-22 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('item', models.CharField(max_length=255)),
                ('location_long', models.DecimalField(decimal_places=6, max_digits=9)),
                ('location_lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.product')),
                ('price_low', models.IntegerField()),
                ('price_high', models.IntegerField()),
            ],
            bases=('app.product',),
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.product')),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
                ('price', models.IntegerField()),
            ],
            bases=('app.product',),
        ),
    ]
