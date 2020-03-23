# Generated by Django 2.2.11 on 2020-03-23 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0010_remove_project_pics_prj_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_pics',
            name='prj_pic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='oproject', to='Project.Projects'),
            preserve_default=False,
        ),
    ]