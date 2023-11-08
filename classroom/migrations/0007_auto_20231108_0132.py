# Generated by Django 3.0.5 on 2023-11-07 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagetoteacher',
            name='reply',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='messagetoteacher',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='classroom.Student'),
        ),
        migrations.AlterField(
            model_name='messagetoteacher',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='classroom.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='messagetoteacher',
            unique_together=set(),
        ),
    ]