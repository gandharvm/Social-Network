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
