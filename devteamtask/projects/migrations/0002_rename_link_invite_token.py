# Generated by Django 4.1.9 on 2023-05-13 13:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invite",
            old_name="link",
            new_name="token",
        ),
    ]