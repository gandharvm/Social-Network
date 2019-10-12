from django.db import models


class MoneyRequest(models.Model):
    amount=models.FloatField(default=0)
    from_user=models.IntegerField(default=0)


class User(models.Model):
    category = models.CharField(max_length=20)
    friends = models.ManyToManyField("self")
    friend_requests = models.ManyToManyField("self")
    wallet_money = models.FloatField(default=0)
    transactions = models.IntegerField(default=0)
    others_can_post = models.BooleanField(default="False")
    username = models.CharField(max_length=50, default="Abc")
    money_requests=models.ManyToManyField(MoneyRequest)

    @classmethod
    def create(cls, username):
        return cls(username=username)

    def send_friend_request(self,UserId):
        to_user=User.objects.get(pk=UserId)
        from_user=self.pk
        to_user.friend_requests.add(from_user)
        self.save()
        to_user.save()

    def accept_friend_request(self, UserId):
        self.friends.add(UserId)
        self.friend_requests.remove(UserId)
        self.save()

    def reject_friend_request(self, UserId):
        self.friend_requests.remove(UserId)
        self.save()

    def deposit_money(self,amount):
        self.wallet_money+=amount
        self.save()
    
    def send_money(self,amount,UserId):
        to_user=User.objects.get(pk=UserId)
        from_user=self.pk
        r=MoneyRequest()
        r.amount=amount
        r.from_user=from_user
        r.save()
        to_user.money_requests.add(r)
        self.save()
        to_user.save()
        

    def accept_money(self,tid):
        r=MoneyRequest.objects.get(pk=tid)
        self.wallet_money+=r.amount
        u=User.objects.get(pk=r.from_user)
        u.transactions+=1
        u.wallet_money-=r.amount
        u.save()
        self.money_requests.remove(tid)
        self.save()

    def reject_money(self,tid):
        self.money_requests.remove(tid)
        self.save()
    
    def __str__(self):
        return ("%s"%self.pk)



    def send_message(self, UserId, content):
        from_user = self
        to_user = User.objects.get(pk=UserId)
        msg = Private_Message(from_user=from_user, to_user=to_user, content=content)
        msg.save()
        return msg

    def __str__(self):
        return self.username


class Friendship(models.Model):
    from_friend = models.ForeignKey(
        User, related_name="friend_set", on_delete=models.CASCADE
    )
    to_friend = models.ForeignKey(
        User, related_name="to_friend_set", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("to_friend", "from_friend"),)


class CasualUser(User):
    pass


class PremiumUser(User):
    pass


class CommercialUser(User):
    pass


class Private_Message(models.Model):
    from_user = models.ForeignKey(
        User, related_name="from_msg", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(User, related_name="to_msg", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)

    def __str__(self):
        return (
            "From "
            + str(self.from_user)
            + " To "
            + str(self.to_user)
            + "\n"
            + self.content
        )

    def __eq__(self, other):
        return str(self) == str(other)
