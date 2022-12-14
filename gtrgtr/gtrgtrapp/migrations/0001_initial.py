# Generated by Django 4.1.2 on 2022-10-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guitars',
            fields=[
                ('incrementingIndex', models.AutoField(primary_key=True, serialize=False)),
                ('itemName', models.CharField(max_length=200)),
                ('brandName', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('salesPrice', models.IntegerField()),
                ('pictureMain', models.URLField()),
                ('qtyInStock', models.IntegerField()),
                ('qtyOnOrder', models.IntegerField()),
                ('colour', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('pickup', models.CharField(max_length=200)),
                ('bodyShape', models.CharField(max_length=200)),
                ('spotifyPreviewURL', models.URLField()),
            ],
        ),
    ]
