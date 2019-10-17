# Generated by Django 2.2.6 on 2019-10-16 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoneyRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('from_user', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('wallet_money', models.FloatField(default=0)),
                ('transactions', models.IntegerField(default=0)),
                ('others_can_post', models.BooleanField(default='False')),
                ('username', models.CharField(default='Abc', max_length=50)),
                ('friend_requests', models.ManyToManyField(related_name='_user_friend_requests_+', to='mainapp.User')),
                ('friends', models.ManyToManyField(related_name='_user_friends_+', to='mainapp.User')),
                ('money_requests', models.ManyToManyField(to='mainapp.MoneyRequest')),
            ],
        ),
        migrations.CreateModel(
            name='CasualUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.User')),
            ],
            bases=('mainapp.user',),
        ),
        migrations.CreateModel(
            name='CommercialUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.User')),
            ],
            bases=('mainapp.user',),
        ),
        migrations.CreateModel(
            name='PremiumUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.User')),
                ('plan', models.CharField(default='silver', max_length=10)),
            ],
            bases=('mainapp.user',),
        ),
        migrations.CreateModel(
            name='Private_Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_msg', to='mainapp.User')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_msg', to='mainapp.User')),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to='mainapp.User')),
                ('to_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_friend_set', to='mainapp.User')),
            ],
            options={
                'unique_together': {('to_friend', 'from_friend')},
            },
        ),
    ]
