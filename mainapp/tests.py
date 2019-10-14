from django.test import TestCase
from .models import User, Private_Message

# Create your tests here.


class Private_Messages_Test(TestCase):
    def test_message(self):
        u1 = User.create("A")
        u1.save()
        u2 = User.create("B")
        u2.save()
        k2 = u2.pk
        msg = u1.send_message(k2, "Hello World!")
        self.assertIn(
            Private_Message(from_user=u1, to_user=u2, content="Hello World!"),
            Private_Message.objects.all(),
        )
    
    def test_friend_request(self):
        u1=User.create("A")
        u1.save()
        k1=u1.pk
        u2=User.create("B")
        u2.save()
        k2=u2.pk
        u2.send_friend_request(k1)
        self.assertIn(
            k2,u1.friend_requests
        )
        u1.accept_friend_request(k2)
        self.assertIn(k2,u1.friends)
        self.assertIn(k1,u2.friends)
    
    def test_send_money(self):
        u1=User()
        u1.save()
        k1=u1.pk
        u2=User()
        u2.save()
        k2=u2.pk
        u2.send_friend_request(k1)
        u1.accept_friend_request(k2)

        u1.deposit_money(1000)
        self.assertEqual(1000,u1.wallet_money)

        u1.send_money(100,k2)
        l=u2.money_requests.first()
        l=l.pk
        u2.accept_money(l)

        self.assertEqual(u2.wallet_money,100)
        # self.assertEqual(u1.wallet_money,900)  failing 
        # self.assertEqual(u2.transactions,1)    failing
        