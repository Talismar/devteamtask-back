# Generated by Django 4.0.8 on 2023-05-11 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='sprint_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.sprint'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.status'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.tag'),
        ),
        migrations.AddField(
            model_name='sprint',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]