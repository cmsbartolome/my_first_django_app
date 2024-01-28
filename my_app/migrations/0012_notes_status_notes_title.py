# Generated by Django 4.2.1 on 2023-12-09 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0011_remove_notes_createdby_notes_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='status',
            field=models.CharField(choices=[('Active', 'active'), ('In-active', 'in-active')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='notes',
            name='title',
            field=models.TextField(blank=True, max_length=160, null=True),
        ),
    ]
