# Generated by Django 5.2.1 on 2025-05-26 19:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPreference",
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
                ("genres", models.JSONField(default=list)),
                ("goals", models.JSONField(default=list)),
                ("reading_time", models.CharField(blank=True, max_length=50)),
                ("reading_duration", models.CharField(blank=True, max_length=50)),
                ("reading_complexity", models.CharField(blank=True, max_length=50)),
                ("favorite_books", models.JSONField(default=list)),
                ("mood", models.JSONField(default=list)),
                ("onboarding_completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preference",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
