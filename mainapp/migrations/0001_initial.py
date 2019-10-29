# Generated by Django 2.2.6 on 2019-10-29 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CasualUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_of_birth', models.DateField()),
                ('email_id', models.EmailField(max_length=254)),
                ('wallet_money', models.FloatField(default=0)),
                ('transactions', models.IntegerField(default=0)),
                ('others_can_post', models.BooleanField(default='False')),
                ('others_can_see_friends', models.BooleanField(default='False')),
                ('others_can_see_email', models.BooleanField(default='False')),
                ('others_can_see_dob', models.BooleanField(default='False')),
                ('friend_requests', models.ManyToManyField(related_name='_casualuser_friend_requests_+', to='mainapp.CasualUser')),
                ('friends', models.ManyToManyField(related_name='_casualuser_friends_+', to='mainapp.CasualUser')),
            ],
        ),
        migrations.CreateModel(
            name='GroupAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='intHolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('from_user', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('time', models.DateTimeField(auto_now=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_by', to='mainapp.CasualUser')),
            ],
        ),
        migrations.CreateModel(
            name='PremiumUser',
            fields=[
                ('casualuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.CasualUser')),
                ('plan', models.CharField(default='silver', max_length=10)),
                ('next_payment_premium', models.DateField(auto_now_add=True)),
            ],
            bases=('mainapp.casualuser',),
        ),
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts', models.ManyToManyField(related_name='timeline', to='mainapp.Post')),
                ('timeline_of', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainapp.CasualUser')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_message', to='mainapp.CasualUser')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New Group', max_length=20)),
                ('max_num_of_members', models.IntegerField(default=20)),
                ('can_send_join_requests', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.GroupAdmin')),
                ('join_requests', models.ManyToManyField(related_name='sent_join_request_to', to='mainapp.CasualUser')),
                ('members', models.ManyToManyField(related_name='member_of', to='mainapp.CasualUser')),
                ('messages', models.ManyToManyField(related_name='message_on', to='mainapp.GroupMessage')),
            ],
        ),
        migrations.AddField(
            model_name='casualuser',
            name='money_requests',
            field=models.ManyToManyField(to='mainapp.MoneyRequest'),
        ),
        migrations.CreateModel(
            name='CommercialUser',
            fields=[
                ('premiumuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.PremiumUser')),
                ('next_payment', models.DateField(auto_now=True)),
            ],
            bases=('mainapp.premiumuser',),
        ),
        migrations.CreateModel(
            name='Private_Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_msg', to='mainapp.CasualUser')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_msg', to='mainapp.PremiumUser')),
            ],
        ),
        migrations.AddField(
            model_name='groupadmin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='mainapp.PremiumUser'),
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to='mainapp.CasualUser')),
                ('to_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_friend_set', to='mainapp.CasualUser')),
            ],
            options={
                'unique_together': {('to_friend', 'from_friend')},
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Content', models.CharField(max_length=500)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.CommercialUser')),
            ],
        ),
    ]
