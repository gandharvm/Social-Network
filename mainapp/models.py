from django.db import models
from math import inf


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
    def paymentCycleInMonths(self):
        return 1
    
    def amountToPay(self):
        return 0
    
    def maxTransactions(self):
        return 15
    
    def toPremium(self,plan):
        fields = [f.name for f in User._meta.fields if f.name != 'id']
        values = dict( [(x, getattr(self, x)) for x in fields] )
        new_instance = PremiumUser(**values)
        # new_instance.User_ptr = self.User_ptr #re-assign related parent
        self.delete()
        new_instance.plan=plan
        new_instance.save()
        return(new_instance)


class PremiumUser(User):
    plansMap={'silver':0,'gold':1,'platinum':1}
    planCosts=[50,100,150]
    plansMaxGroups=[2,4,inf]
    plan = models.CharField(max_length=10, default="silver")
    
    def amountToPay(self):
        return(planCosts[plansMap[self.plan.lower()]])
    
    def paymentCycleInMonths(self):
        return 1
    
    def maxTransactions(self):
        return 30
    
    def maxGroups(self):
        return(plansMaxGroups[plansMap[self.plan.lower()]])


class CommercialUser(User):
    def amountToPay(self):
        return 5000
    
    def paymentCycleInMonths(self):
        return 12
    
    def maxTransactions(self):
        return inf


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
