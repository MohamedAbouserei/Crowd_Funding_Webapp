# Generated by Django 2.2.11 on 2020-03-26 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0018_auto_20200326_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_user_comment_post',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scomment', to='Project.Project_comments'),
        ),
    ]