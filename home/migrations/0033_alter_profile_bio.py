# Generated by Django 5.0.3 on 2024-05-03 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
