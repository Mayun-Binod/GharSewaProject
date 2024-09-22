# Generated by Django 3.2 on 2021-06-17 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('content', models.TextField()),
                ('timeStamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]