# Generated by Django 2.2.6 on 2019-10-12 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20191002_0604'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiumuser',
            name='plan',
            field=models.CharField(default='silver', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='others_can_post',
            field=models.BooleanField(default='False'),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='Abc', max_length=50),
        ),
        migrations.CreateModel(
            name='Private_Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_msg', to='mainapp.User')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_msg', to='mainapp.User')),
            ],
        ),
    ]
