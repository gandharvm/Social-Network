# Generated by Django 2.2.4 on 2019-10-30 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20191030_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='can_join_directly',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='can_see_group_members',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='can_send_join_requests',
            field=models.BooleanField(default=True),
        ),
    ]
