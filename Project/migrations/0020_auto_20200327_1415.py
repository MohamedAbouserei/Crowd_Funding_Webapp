# Generated by Django 2.2.11 on 2020-03-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0019_auto_20200326_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_user_comment_post',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='project_user_comment_post',
            name='like',
        ),
        migrations.AddField(
            model_name='project_user_comment_post',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
