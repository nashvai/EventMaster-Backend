# Generated by Django 5.1.1 on 2024-10-28 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Eventmaster", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("date", models.DateTimeField()),
                ("description", models.TextField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_events",
                        to="Eventmaster.event",
                    ),
                ),
            ],
        ),
    ]