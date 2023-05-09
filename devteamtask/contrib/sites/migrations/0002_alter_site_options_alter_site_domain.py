# Generated by Django 4.1.9 on 2023-05-09 01:43

import django.contrib.sites.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="site",
            options={"ordering": ["domain"], "verbose_name": "site", "verbose_name_plural": "sites"},
        ),
        migrations.AlterField(
            model_name="site",
            name="domain",
            field=models.CharField(
                max_length=100,
                unique=True,
                validators=[django.contrib.sites.models._simple_domain_name_validator],
                verbose_name="domain name",
            ),
        ),
    ]
