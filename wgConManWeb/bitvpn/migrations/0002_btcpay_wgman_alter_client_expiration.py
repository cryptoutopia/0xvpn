# Generated by Django 4.1.1 on 2022-10-02 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitvpn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BtcPay',
            fields=[
                ('pickle', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'btcpay',
            },
        ),
        migrations.CreateModel(
            name='Wgman',
            fields=[
                ('pickle', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'wgman',
            },
        ),
        migrations.AlterField(
            model_name='client',
            name='expiration',
            field=models.DateTimeField(),
        ),
    ]
