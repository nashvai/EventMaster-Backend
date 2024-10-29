# Generated by Django 5.1.1 on 2024-10-28 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Eventmaster", "0003_rename_title_subevent_titles"),
    ]

    operations = [
        migrations.RenameField(
            model_name="subevent", old_name="titles", new_name="title",
        ),
        migrations.CreateModel(
            name="Component",
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
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=100)),
                ("quantity", models.IntegerField()),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "sub_event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="components",
                        to="Eventmaster.subevent",
                    ),
                ),
            ],
        ),
    ]
