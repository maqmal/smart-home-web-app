# Generated by Django 3.1.5 on 2021-01-29 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0015_auto_20210129_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='ai_enable',
            new_name='rectangle_box',
        ),
    ]