# Generated by Django 4.2.1 on 2023-10-27 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0008_alter_notes_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='createdBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]