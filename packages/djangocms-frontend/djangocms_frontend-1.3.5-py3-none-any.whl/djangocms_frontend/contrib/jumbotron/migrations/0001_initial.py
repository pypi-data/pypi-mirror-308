# Generated by Django 3.2.11 on 2022-01-12 21:04

from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("djangocms_frontend", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Jumbotron",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
                "verbose_name": "Jumbotron",
            },
            bases=("djangocms_frontend.frontenduiitem",),
        ),
    ]
