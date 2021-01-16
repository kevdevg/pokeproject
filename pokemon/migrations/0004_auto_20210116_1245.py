# Generated by Django 3.1.5 on 2021-01-16 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0003_auto_20210116_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='stats',
        ),
        migrations.AddField(
            model_name='pokemonstats',
            name='pokemon',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pokemon.pokemon'),
            preserve_default=False,
        ),
    ]
