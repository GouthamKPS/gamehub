# Generated by Django 5.0.4 on 2024-11-02 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameApp', '0009_library_libraryitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
