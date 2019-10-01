from django.db import models

class MoneyRequest(models.Model):
    pass

class User(models.Model):
    category=models.CharField(max_length=20)
    friends=models.ManyToManyField("self")
    friend_requests=models.ManyToManyField("self")
    wallet_money=models.FloatField(default=0)
    transactions=models.IntegerField(default=0)

    def send_friend_request(self,UserId):
        to_user=User.objects.get(pk=UserId)
        from_user=self.pk
        to_user.friend_requests.add(from_user)
    
    def accept_friend_request(self,UserId):
        self.friends.add(UserId)
        self.friend_requests.remove(UserId)

    def reject_friend_request(self,UserId):
        self.friend_requests.remove(UserId)

    def deposit_money(self,amount):
        self.wallet_money+=amount
    
    def send_money(self,amount,UserId):



class Friendship(models.Model):
    from_friend=models.ForeignKey(User,related_name='friend_set',on_delete=models.CASCADE)
    to_friend=models.ForeignKey(User,related_name='to_friend_set',on_delete=models.CASCADE)
    class Meta:
        unique_together = (('to_friend', 'from_friend'), )  


class CasualUser(User):
    pass

class PremiumUser(User):
    pass

class CommercialUser(User):
    pass