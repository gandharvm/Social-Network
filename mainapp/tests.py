from django.test import TestCase
from .models import *
from datetime import datetime


class Private_Messages_Test(TestCase):
    def test_message(self):
        u1 = User.create("A", datetime.today(), 'a@x.com')
        u2 = User.create("B", datetime.today(), 'b@x.com')
        k2 = u2.pk
        msg = u1.send_message(k2, "Hello World!")
        self.assertIn(
            Private_Message(from_user=u1, to_user=u2, content="Hello World!"),
            Private_Message.objects.all(),
        )


class User_Test(TestCase):
    def test_friend_request(self):
        u1 = User.create("C", datetime.today(), 'c@x.com')
        k1 = u1.pk
        u2 = User.create("D", datetime.today(), 'd@x.com')
        k2 = u2.pk
        u2.send_friend_request(k1)
        self.assertIn(
            u2, u1.friend_requests.all()
        )
        u1.accept_friend_request(k2)
        self.assertIn(u2, u1.friends.all())
        self.assertIn(u1, u2.friends.all())

    def test_send_money(self):
        u1 = User.create('E', datetime.today(), 'e@x.com')
        k1 = u1.pk
        u2 = User.create('F', datetime.today(), 'f@x.com')
        k2 = u2.pk
        u2.send_friend_request(k1)
        u1.accept_friend_request(k2)

        u1.deposit_money(1000)
        self.assertEqual(1000, u1.wallet_money)

        u1.send_money(100, k2)
        money_request = u2.money_requests.first()
        money_request = money_request.pk
        u2.accept_money(money_request)

        u1 = User.objects.get(pk=k1)

        self.assertEqual(u2.wallet_money, 100)
        self.assertEqual(u1.wallet_money, 900)
        self.assertEqual(u1.transactions, 1)

    def test_posts(self):
        u1 = User.create('E', datetime.today(), 'e@x.com')
        u1.others_can_post = True
        u2 = User.create('F', datetime.today(), 'f@x.com')
        u2.send_friend_request(u1.pk)
        u1.accept_friend_request(u2.pk)
        post1 = u1.post_on_own_timeline('Hello World. Post on own timeline')
        post2 = u2.post_on_own_timeline('Hello World2. Post on own timeline2')
        post3 = u1.post_on_other_timeline(
            u2.pk, 'Cannot post on others timeline')
        post4 = u2.post_on_other_timeline(u1.pk, 'Post on other timeline')
        timeline1 = Timeline.objects.get(timeline_of=u1)
        timeline2 = Timeline.objects.get(timeline_of=u2)

        self.assertIn(post1, Post.objects.all())
        self.assertIn(post1, timeline1.posts.all())
        self.assertIn(post2, Post.objects.all())
        self.assertIn(post2, timeline2.posts.all())
        self.assertNotIn(post3, Post.objects.all())
        self.assertNotIn(post3, timeline2.posts.all())
        self.assertIn(post4, Post.objects.all())
        self.assertIn(post4, timeline1.posts.all())
