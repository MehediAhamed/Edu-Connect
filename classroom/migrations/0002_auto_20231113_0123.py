# Generated by Django 2.2.12 on 2023-11-12 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentsinclass',
            unique_together={('teacher', 'student', 'subject_name')},
        ),
    ]