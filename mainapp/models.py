from django.db import models
from math import inf
import logging
import datetime

logger = logging.getLogger('MAINAPP')


class MoneyRequest(models.Model):
    amount = models.FloatField(default=0)
    from_user = models.IntegerField(default=0)


class User(models.Model):
    category = models.CharField(max_length=20)
    money_requests = models.ManyToManyField(MoneyRequest)
    username = models.CharField(max_length=30, unique=True)

    # private info
    date_of_birth = models.DateField(default=datetime.date.today)
    email_id = models.EmailField()
    friends = models.ManyToManyField("self")
    friend_requests = models.ManyToManyField("self")
    wallet_money = models.FloatField(default=0)
    transactions = models.IntegerField(default=0)

    # privacy settings
    others_can_post = models.BooleanField(default="False")
    others_can_see_friends = models.BooleanField(default='False')
    others_can_see_email = models.BooleanField(default='True')
    others_can_see_dob = models.BooleanField(default='False')

    @classmethod
    def create(cls, username, dob, email_id):
        # logger.info("user " + username + " created")
        user = cls(username=username, date_of_birth=dob, email_id=email_id)
        user.save()
        timeline = Timeline(timeline_of=user)
        timeline.save()
        return user

    def send_friend_request(self, UserId):
        to_user = User.objects.get(pk=UserId)
        from_user = self.pk
        to_user.friend_requests.add(from_user)
        # logger.info('user '+str(self) +
        #             ' sent friend request to '+str(to_user))
        self.save()
        to_user.save()

    def accept_friend_request(self, UserId):
        self.friends.add(UserId)
        self.friend_requests.remove(UserId)
        # logger.info('user '+str(User.objects.get(pk=UserId)) +
        #             ' and '+str(self)+' are friends')
        self.save()

    def reject_friend_request(self, UserId):
        self.friend_requests.remove(UserId)
        # logger.info('user '+str(self) + ' rejected friend request from ' +
        #             str(User.objects.get(pk=UserId)))
        self.save()

    def deposit_money(self, amount):
        self.wallet_money += amount
        logger.info(str(self)+' deposited '+str(amount)+' to their wallet')
        self.save()

    def send_money(self, amount, UserId):
        to_user = User.objects.get(pk=UserId)
        from_user = self.pk
        r = MoneyRequest(amount=amount, from_user=from_user)
        r.save()
        to_user.money_requests.add(r)
        logger.info(str(self)+' sent money request to ' +
                    str(to_user)+' for '+str(amount)+' amount')
        self.save()
        to_user.save()

    def accept_money(self, tid):
        r = MoneyRequest.objects.get(pk=tid)
        u = User.objects.get(pk=r.from_user)
        u.transactions += 1
        u.wallet_money -= r.amount
        self.wallet_money += r.amount
        u.save()
        self.money_requests.remove(tid)
        logger.info(str(self)+' accepted money request from ' +
                    str(u)+' for '+str(r.amount)+' amount')
        self.save()

    def reject_money(self, tid):
        self.money_requests.remove(tid)
        r = MoneyRequest.objects.get(pk=tid)
        u = User.objects.get(pk=r.from_user)
        logger.info(str(self)+' rejected money request from ' +
                    str(u)+' for '+str(r.amount)+' amount')
        self.save()

    def send_message(self, UserId, content):
        from_user = self
        to_user = User.objects.get(pk=UserId)
        msg = Private_Message(from_user=from_user,
                              to_user=to_user, content=content)
        msg.save()
        return msg

    def post_on_own_timeline(self, content):
        post = Post(posted_by=self, content=content, posted_on=self)
        post.save()
        timeline = Timeline.objects.get(timeline_of=self)
        timeline.posts.add(post)
        timeline.save()
        return post

    def post_on_other_timeline(self, UserId, content):
        user = User.objects.get(pk=UserId)
        post = Post(posted_by=self, content=content, posted_on=user)
        if(user.others_can_post and self in user.friends.all()):
            post.save()
            print(post.pk)
            timeline = Timeline.objects.get(timeline_of=user)
            timeline.posts.add(post)
            timeline.save()
        else:
            # cannot post on this user's timeline
            pass
        return post

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

    def toPremium(self, plan):
        fields = [f.name for f in User._meta.fields if f.name != 'id']
        values = dict([(x, getattr(self, x)) for x in fields])
        new_instance = PremiumUser(**values)
        # new_instance.User_ptr = self.User_ptr #re-assign related parent
        self.delete()
        new_instance.plan = plan
        new_instance.save()
        return(new_instance)


class PremiumUser(User):
    plansMap = {'silver': 0, 'gold': 1, 'platinum': 1}
    planCosts = [50, 100, 150]
    plansMaxGroups = [2, 4, inf]
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
    to_user = models.ForeignKey(
        User, related_name="to_msg", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)

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


class Post(models.Model):
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posted_by')
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)
    posted_on = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posted_on')

    def __str__(self):
        return (self.content)


class Timeline(models.Model):
    timeline_of = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)


class Page(models.Model):
    admin = models.ManyToManyField(CommercialUser)
    Content = models.CharField(max_length=500)
