# Generated by Django 4.1.9 on 2023-05-24 14:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="end_data",
            new_name="end_date",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="start_data",
            new_name="start_date",
        ),
    ]