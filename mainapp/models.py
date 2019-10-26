from django.db import models
from math import inf
import logging

logger = logging.getLogger('MAINAPP')


class MoneyRequest(models.Model):
    amount = models.FloatField(default=0)
    from_user = models.IntegerField(default=0)


class CasualUser(models.Model):
    category = models.CharField(max_length=20)
    money_requests = models.ManyToManyField(MoneyRequest)
    username = models.CharField(max_length=30, unique=True)
    max_transactions = 15

    # private info
    date_of_birth = models.DateField()
    email_id = models.EmailField()
    friends = models.ManyToManyField("self")
    pot_friends=models.ManyToManyField("self")
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
        to_user = CasualUser.objects.filter(pk=UserId)
        if not to_user.exists():
            return
        to_user = to_user[0]
        self.pot_friends.add(to_user);
        from_user = self
        to_user.friend_requests.add(from_user)
        # logger.info('user '+str(self) +
        #             ' sent friend request to '+str(to_user))
        self.save()
        to_user.save()

    def accept_friend_request(self, UserId):
        fr = self.friend_requests.filter(pk=UserId)
        k=CasualUser.objects.get(pk=UserId)
        if not fr.exists():
            return
        self.friends.add(UserId)
        k.pot_friends.remove(self)
        self.friend_requests.remove(UserId)
        self.save()
        k.save()

    def reject_friend_request(self, UserId):
        fr = self.friend_requests.filter(pk=UserId)
        if not fr.exists():
            return
        self.friend_requests.remove(UserId)
        self.save()
    
    def unfriend(self,UserId):
        fr = self.friend_requests.filter(pk=UserId)
        k=CasualUser.objects.get(pk=UserId)
        if not fr.exists():
            return
        self.friends.remove(fr)
        k.friends.remove(self)
        self.save()
        k.save()

    def deposit_money(self, amount):
        self.wallet_money += amount
        logger.info(str(self)+' deposited '+str(amount)+' to their wallet')
        self.save()

    def send_money(self, amount, UserId):
        if(self.transactions < self.max_transactions):
            to_user = self.friends.filter(pk=UserId)
            if not to_user.exists():
                return
            to_user = to_user[0]
            from_user = self.pk
            r = MoneyRequest(amount=amount, from_user=from_user)
            r.save()
            to_user.money_requests.add(r)
            logger.info(str(self)+' sent money request to ' +
                        str(to_user)+' for '+str(amount)+' amount')
            self.save()
            to_user.save()

    def accept_money(self, tid):
        r = self.money_requests.filter(pk=tid)
        if not r.exists():
            return
        r = r[0]
        u = CasualUser.objects.filter(pk=r.from_user)
        if not u.exists():
            self.money_requests.remove(tid)
            r.delete()
            self.save()
        else:
            u = u[0]
            if u.transactions < u.max_transactions:
                u.transactions += 1
                u.wallet_money -= r.amount
                self.wallet_money += r.amount
                u.save()
                self.money_requests.remove(tid)
                r.delete()
                logger.info(str(self)+' accepted money request from ' +
                            str(u)+' for '+str(r.amount)+' amount')
                self.save()

    def reject_money(self, tid):
        r = MoneyRequest.objects.filter(pk=tid)
        if not r.exists():
            return
        r = r[0]
        self.money_requests.remove(tid)
        r.delete()
        if r.from_user in CasualUser.objects.all():
            u = u[0]
            logger.info(str(self)+' rejected money request from ' +
                        str(u)+' for '+str(r.amount)+' amount')
        self.save()

    def post_on_own_timeline(self, content):
        post = Post(posted_by=self, content=content)
        post.save()
        timeline = Timeline.objects.get(timeline_of=self)
        timeline.posts.add(post)
        timeline.save()
        return post

    def post_on_other_timeline(self, UserId, content):
        user = self.friends.filter(pk=UserId)
        if not user.exists():
            return
        user = user[0]
        post = Post(posted_by=self, content=content)
        if(user.others_can_post):
            post.save()
            timeline = Timeline.objects.get(timeline_of=user)
            timeline.posts.add(post)
            timeline.save()
        else:
            # cannot post on this user's timeline
            pass
        return post

    def __str__(self):
        return self.username

    def send_join_request(self, GroupId):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        if(group.can_send_join_requests):
            group.join_requests.add(self)
            group.save()

    def paymentCycleInMonths(self):
        return 1

    def amountToPay(self):
        return 0

    def maxTransactions(self):
        return max_transactions

    def toPremium(self, plan):
        fields = [f.name for f in CasualUser._meta.fields if f.name != 'id']
        values = dict([(x, getattr(self, x)) for x in fields])
        new_instance = PremiumUser(**values)
        # new_instance.User_ptr = self.User_ptr #re-assign related parent
        self.delete()
        new_instance.plan = plan
        new_instance.save()
        return(new_instance)


class Friendship(models.Model):
    from_friend = models.ForeignKey(
        CasualUser, related_name="friend_set", on_delete=models.CASCADE
    )
    to_friend = models.ForeignKey(
        CasualUser, related_name="to_friend_set", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("to_friend", "from_friend"),)


class PremiumUser(CasualUser):
    plansMap = {'silver': 0, 'gold': 1, 'platinum': 1}
    planCosts = [50, 100, 150]
    plansMaxGroups = [2, 4, inf]
    plan = models.CharField(max_length=10, default="silver")
    max_transactions = 30

    @classmethod
    def create(cls, username, dob, email_id, plan):
        # logger.info("user " + username + " created")
        user = cls(username=username, date_of_birth=dob,
                   email_id=email_id, plan=plan)
        user.save()
        timeline = Timeline(timeline_of=user)
        timeline.save()
        return user

    def amountToPay(self):
        return(planCosts[plansMap[self.plan.lower()]])

    def paymentCycleInMonths(self):
        return 1

    def maxTransactions(self):
        return max_transactions

    def maxGroups(self):
        return(plansMaxGroups[plansMap[self.plan.lower()]])

    def create_group(self, group_name):
        if(self in GroupAdmin.objects.all()):
            admin = GroupAdmin.objects.get(user=self)
        else:
            admin = GroupAdmin(user=self)
            admin.save()
        admin.create_group(username)

    def send_message(self, UserId, content):
        to_user = self.friends.filter(pk=UserId)
        if not to_user.exists():
            return
        to_user = to_user[0]
        from_user = self
        msg = Private_Message(from_user=from_user,
                              to_user=to_user, content=content)
        msg.save()
        return msg


class CommercialUser(PremiumUser):
    max_transactions = inf

    @classmethod
    def create(cls, username, dob, email_id, plan):
        # logger.info("user " + username + " created")
        user = cls(username=username, date_of_birth=dob,
                   email_id=email_id, plan=plan)
        user.save()
        timeline = Timeline(timeline_of=user)
        timeline.save()
        return user

    def amountToPay(self):
        return 5000

    def paymentCycleInMonths(self):
        return 12

    def maxTransactions(self):
        return max_transactions

    def create_page(self, content):
        page = Page(admin, content=content)
        page.save()

    def send_message(self, UserId, content):
        to_user = CasualUser.objects.filter(pk=UserId)
        if not to_user.exists():
            return
        to_user = to_user[0]
        from_user = self
        msg = Private_Message(from_user=from_user,
                              to_user=to_user, content=content)
        msg.save()
        return msg


class Private_Message(models.Model):
    from_user = models.ForeignKey(
        PremiumUser, related_name="from_msg", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CasualUser, related_name="to_msg", on_delete=models.CASCADE)
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
        CasualUser, on_delete=models.CASCADE, related_name='posted_by')
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.content)


class Timeline(models.Model):
    timeline_of = models.OneToOneField(CasualUser, on_delete=models.CASCADE)
    posts = models.ManyToManyField(
        Post, related_name='timeline')


class Page(models.Model):
    admin = models.ForeignKey(CommercialUser, on_delete=models.CASCADE)
    Content = models.CharField(max_length=500)


class GroupAdmin(models.Model):
    user = models.OneToOneField(
        PremiumUser, on_delete=models.CASCADE, related_name='user')
    group_count = 0

    def create_group(self, group_name, max_num, can_send):
        if(max_num < 3):
            max_num = 20
        if user.group_count <= user.plansMaxGroups[plansMap[plan]]:
            group = Group(admin=self, name=group_name,
                          max_num_of_members=max_num,
                          can_send_join_requests=can_send)
            group_count += 1
            self.save()
            group.save()

    def delete_group(self, GroupId):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        if group.admin == self:
            group.delete()
            self.group_count -= 1
            self.save()
        else:
            return

    def add_member(self, UserId, GroupId):
        user = CasualUser.objects.filter(pk=UserId)
        if not user.exists():
            return
        user = user[0]
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        if group.admin == self:
            group.members.add(user)
            group.save()

    def remove_member(self, UserId, GroupId):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        user = group.members.filter(pk=UserId)
        if not user.exists():
            return
        user = user[0]
        if group.admin == self:
            group.members.remove(UserId)
            group.save()

    def accept_join_request(self, GroupId, joinId):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        user = group.join_requests.filter(pk=joinId)
        if group.admin == self:
            if not user.exists() or user not in CasualUser.objects.all():
                return

            user = user[0]
            group.members.add(user)
            group.join_requests.remove(UserId)
            group.save()

    def reject_join_request(self, GroupId, joinId):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        user = group.join_requests.filter(pk=joinId)
        if group.admin == self:
            if not user.exists():
                return

            user = user[0]
            group.join_requests.remove(UserId)
            group.save()

    def inc_people(self, GroupId, num):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        if group.admin == self and num > group.max_num_of_members:
            group.max_num_of_members = num

    def change_join_settings(self, GroupId, setting):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return
        group = group[0]
        if(group.admin == self):
            group.can_send_join_requests = setting

class intHolder(models.Model):
    num=models.IntegerField(default=0)

class Group(models.Model):
    admin = models.ForeignKey(GroupAdmin, on_delete=models.CASCADE)
    members = models.ManyToManyField(CasualUser, related_name='member_of')
    name = models.CharField(max_length=20, default='New Group')
    join_requests = models.ManyToManyField(
        CasualUser, related_name='sent_join_request_to')
    max_num_of_members = models.IntegerField(default=20)
    can_send_join_requests = models.BooleanField(default=False)