# Generated by Django 3.1.5 on 2021-01-12 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]