from django.db import models
from math import inf
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('MAINAPP')


class MoneyRequest(models.Model):
    amount = models.FloatField(default=0)
    from_user = models.IntegerField(default=0)


class CasualUser(models.Model):
    category = models.CharField(max_length=20)
    money_requests = models.ManyToManyField(MoneyRequest)
    username = models.CharField(max_length=30)
    max_transactions = 15

    # private info
    date_of_birth = models.DateField()
    email_id = models.EmailField()
    friends = models.ManyToManyField("self")
    friend_requests = models.ManyToManyField("self")
    wallet_money = models.FloatField(default=0)
    transactions = models.IntegerField(default=0)

    # privacy settings
    others_can_post = models.BooleanField(default="False")
    others_can_see_friends = models.BooleanField(default='False')
    others_can_see_email = models.BooleanField(default='False')
    others_can_see_dob = models.BooleanField(default='False')

    @classmethod
    def create(cls, username, dob, email_id):
        # logger.info("user " + username + " created")
        user = cls(username=username, date_of_birth=dob, email_id=email_id)
        user.category="casual"
        user.save()
        timeline = Timeline(timeline_of=user)
        timeline.save()
        return user

    def send_friend_request(self, UserId):
        to_user = CasualUser.objects.filter(pk=UserId)
        if not to_user.exists():
            return 'User does not exist'
        to_user = to_user[0]
        from_user = self
        if(from_user in to_user.friend_requests.all()):
            return 'Friend request already sent'
        if(from_user in to_user.friend_set.all()):
            return 'User is already a friend'
        to_user.friend_requests.add(from_user)
        # logger.info('user '+str(self) +
        #             ' sent friend request to '+str(to_user))
        self.save()
        to_user.save()
        return 'Friend request sent'

    def unfriend(self, UserId):
        fr = self.friends.filter(pk=UserId)
        if not fr.exists():
            return 'User is not a friend'
        fr = fr[0]
        self.friends.remove(fr)
        fr.friends.remove(self)
        self.save()
        fr.save()
        return 'User unfriended'

    def accept_friend_request(self, UserId):
        fr = self.friend_requests.filter(pk=UserId)
        if not fr.exists():
            return 'No such friend request'
        self.friends.add(UserId)
        self.friend_requests.remove(UserId)
        self.save()
        return 'friend request accepted'

    def reject_friend_request(self, UserId):
        fr = self.friend_requests.filter(pk=UserId)
        if not fr.exists():
            return 'Friend request does not exist'
        self.friend_requests.remove(UserId)
        self.save()
        return 'Friend request rejected'

    def deposit_money(self, amount):
        if(amount > 0 and amount <= 10000000):
            self.wallet_money += amount
            logger.info(str(self)+' deposited '+str(amount)+' to their wallet')
            self.save()
            return "Amount added to wallet"
        else:
            return 'Amount invalid'

    def send_money(self, amount, UserId):
        if(self.transactions < self.max_transactions):
            to_user = self.friends.filter(pk=UserId)
            if not to_user.exists():
                return 'User does not exist'
            to_user = to_user[0]
            from_user = self.pk
            if(amount <= 0 or amount > 1000000):
                return 'Amount invalid'
            r = MoneyRequest(amount=amount, from_user=from_user)
            r.save()
            to_user.money_requests.add(r)
            logger.info(str(self)+' sent money request to ' +
                        str(to_user)+' for '+str(amount)+' amount')
            self.save()
            to_user.save()
            return 'Money Request sent'

    def accept_money(self, tid):
        r = self.money_requests.filter(pk=tid)
        if not r.exists():
            return 'Money request does not exist'
        r = r[0]
        u = CasualUser.objects.filter(pk=r.from_user)
        if not u.exists():
            self.money_requests.remove(tid)
            r.delete()
            self.save()
            return 'User does not exist'
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
            return 'Money request exceeded'
        else:
            return 'Sender has exceeded his max limit of transactions'

    def reject_money(self, tid):
        r = MoneyRequest.objects.filter(pk=tid)
        if not r.exists():
            return 'Money request does not exist'
        r = r[0]
        self.money_requests.remove(tid)
        r.delete()
        if r.from_user in CasualUser.objects.all():
            u = u[0]
            logger.info(str(self)+' rejected money request from ' +
                        str(u)+' for '+str(r.amount)+' amount')
        self.save()
        return 'Money request deleted'

    def post_on_own_timeline(self, content):
        post = Post(posted_by=self, content=content)
        post.save()
        timeline = Timeline.objects.get(timeline_of=self)
        timeline.posts.add(post)
        timeline.save()
        return 'Successfully posted on timeline'

    def post_on_other_timeline(self, UserId, content):
        user = self.friends.filter(pk=UserId)
        if not user.exists():
            return 'User does not exist'
        user = user[0]
        post = Post(posted_by=self, content=content)
        if(user.others_can_post):
            post.save()
            timeline = Timeline.objects.get(timeline_of=user)
            timeline.posts.add(post)
            timeline.save()
        else:
            return "You cannot post on this user's timeline"
        return 'Posted on timeline'

    def __str__(self):
        return self.username

    def send_join_request(self, GroupId):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return 'group does not exist'
        group = group[0]
        if(group.can_send_join_requests):
            group.join_requests.add(self)
            group.save()
            return 'sent join request'
        else:
            return 'cannot send join request to this group'

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
        new_instance.plan = plan
        self.username="!!!" 
        self.save()
        new_instance.save()
        fk=MoneyRequest.objects.filter(from_user=self.pk)
        if(fk.exists()):
            for request in fk:
                request.from_user=new_instance.pk
                request.save()
        
        fk=Private_Message.objects.filter(from_user=self)
        if(fk.exists()):
            for request in fk:
                request.from_user=new_instance
                request.save()
        
        fk=Private_Message.objects.filter(to_user=self)
        if(fk.exists()):
            for request in fk:
                request.to_user=new_instance
                request.save()
        
        fk=Post.objects.filter(posted_by=self)
        if(fk.exists()):
            for request in fk:
                request.posted_by=new_instance
                request.save()
        
        fk=Timeline.objects.filter(timeline_of=self)
        if(fk.exists()):
            for request in fk:
                request.timeline_of=new_instance
                request.save()
        
        fk=GroupMessage.objects.filter(from_user=self)
        if(fk.exists()):
            for request in fk:
                request.from_user=new_instance
                request.save()
        
        fk=Group.objects.all()
        for group in fk:
            fk2=group.members.filter(pk=self.pk)
            if(fk2.exists()):
                for mem in fk2:
                    mem=new_instance
            group.save()

        self.delete()
        return(new_instance)

    def send_message_on_group(self, GroupId, content):
        group = Group.objects.filter(pk=GroupId)
        if not group.exists():
            return 'Group does not exist'
        group = group[0]
        if self not in group.members.all():
            return 'You are not a member of the group'
        message = GroupMessage(from_user=self, content=content)
        message.save()
        group.messages.add(message)
        group.save()
        return 'Message sent'


class Friendship(models.Model):
    from_friend = models.ForeignKey(
        CasualUser, related_name="friend_set", on_delete=models.CASCADE
    )
    to_friend = models.ForeignKey(
        CasualUser, related_name="to_friend_set", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("to_friend", "from_friend"),)


class intHolder(models.Model):
    num = models.IntegerField(default=0)


class PremiumUser(CasualUser):
    plansMap = {'silver': 0, 'gold': 1, 'platinum': 1}
    planCosts = [50, 100, 150]
    plansMaxGroups = [2, 4, inf]
    plan = models.CharField(max_length=10, default="silver")
    max_transactions = 30
    next_payment_premium = models.DateField(auto_now_add=True)
    group_count = models.IntegerField(default=0)

    @classmethod
    def create(cls, username, dob, email_id, plan):
        # logger.info("user " + username + " created")
        user = cls(username=username, date_of_birth=dob,
                   email_id=email_id, plan=plan)
        user.category = "premium"
        user.save()
        timeline = Timeline(timeline_of=user)
        timeline.save()
        return user

    def check_pay(self):
        return(datetime.date(datetime.now()) < self.next_payment_premium)

    def amountToPay(self):
        return(self.planCosts[self.plansMap[self.plan.lower()]])

    def paymentCycleInMonths(self):
        return 1

    def maxTransactions(self):
        return max_transactions

    def maxGroups(self):
        return(plansMaxGroups[plansMap[self.plan.lower()]])

    def create_group(self, group_name, can_send, price):
        if(self.check_pay()):
            if self.group_count <= self.plansMaxGroups[self.plansMap[self.plan]]:
                group = Group(admin=self, name=group_name,
                              can_send_join_requests=can_send, price=price)
                self.group_count += 1
                self.save()
                group.save()
                return 'Group created'
            return 'Cannot create more groups'
        else:
            if(self.pay()):
                x = self.create_group(self, group_name, can_send, price)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def change_price(self, GroupId, new_price):
        if(self.check_pay()):
            group = Group.objects.filter(pk=GroupId)
            if not group.exists():
                return 'Group does not exist'
            group = group[0]
            if(group.admin == self):
                group.price = new_price
                return 'Changed price for joining group'
            else:
                return 'You are not admin of this group'
        else:
            if(self.pay()):
                x = self.change_price(self, GroupId, new_price)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def change_name(self, GroupId, new_name):
        if(self.check_pay()):
            group = Group.objects.filter(pk=GroupId)
            if not group.exists():
                return 'Group does not exist'
            group = group[0]
            if(group.admin == self):
                group.name = new_name
                return 'Changed the name of the group'
            else:
                return 'You are not admin of the group'
        else:
            if(self.pay()):
                x = self.change_name(self, GroupId, new_name)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def change_join_settings(self, GroupId, setting):
        if(self.check_pay()):
            group = Group.objects.filter(pk=GroupId)
            if not group.exists():
                return 'Group does not exist'
            group = group[0]
            if(group.admin == self):
                group.can_send_join_requests = setting
                return 'Changed the setting for the group'
            else:
                return 'You are not admin of this group'
        else:
            if(self.pay()):
                x = self.change_join_settings(self, GroupId, setting)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def reject_join_request(self, GroupId, joinId):
        if(self.check_pay()):
            group = Group.objects.filter(pk=GroupId)
            if not group.exists():
                return 'Group does not exist'
            group = group[0]
            user = group.join_requests.filter(pk=joinId)
            if group.admin == self:
                if not user.exists():
                    return 'Join request does not exist'
                user = user[0]
                group.join_requests.remove(user)
                group.save()
                return 'rejected the join request'
            else:
                return 'You are not admin of this group'
        else:
            if(self.pay()):
                x = self.reject_join_request(self, GroupId, joinId)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def accept_join_request(self, GroupId, joinId):
        if(self.check_pay()):
            group = Group.objects.filter(pk=GroupId)
            if not group.exists():
                return 'Group does not exist'
            group = group[0]
            user = group.join_requests.filter(pk=joinId)
            if group.admin == self:
                if (not user.exists()):
                    return 'Join request does not exist'
                if (user[0] not in CasualUser.objects.all()):
                    return 'User does not exist'
                user = user[0]
                if(user.wallet_money < group.price):
                    return 'User does not have enough money'
                user.wallet_money -= group.price
                self.wallet_money += group.price
                group.members.add(user)
                group.join_requests.remove(user)
                group.save()
                self.save()
                return 'Accepted the join request'
            else:
                return 'You are not admin of this group'
        else:
            if(self.pay()):
                x = self.accept_join_request(self, GroupId, joinId)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def remove_member(self, UserId, GroupId):
        if(self.check_pay()):
            group = Group.objects.filter(pk=GroupId)
            if not group.exists():
                return 'Group does not exist'
            group = group[0]
            user = group.members.filter(pk=UserId)
            if not user.exists():
                return 'Member does not exist'
            user = user[0]
            if group.admin == self:
                group.members.remove(user)
                group.save()
                return 'member removed'
            else:
                return 'You are not admin of this group'
        else:
            if(self.pay()):
                x = self.remove_member(self, UserId, GroupId)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def delete_group(self, GroupId):
        if(self.check_pay()):
            group = Group.objects.filter(pk=GroupId)
            if not group.exists():
                return 'Group does not exist'
            group = group[0]
            if group.admin == self:
                group.delete()
                self.group_count += 1
                self.save()
                return 'Deleted the group'
            else:
                return 'You are not admin of this group'
        else:
            if(self.pay()):
                x = self.delete_group(self, joinId)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def send_message(self, UserId, content):
        if(self.check_pay()):
            to_user = self.friends.filter(pk=UserId)
            if not to_user.exists():
                return 'User does not exist'
            to_user = to_user[0]
            from_user = self
            msg = Private_Message(from_user=from_user,
                                  to_user=to_user, content=content)
            msg.save()
            return 'Message sent'
        else:
            if(self.pay()):
                x = self.send_message(UserId, content)
                return 'The Amount due for continued service deducted from your wallet\n'+x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def pay(self):
        if(self.wallet_money > self.amountToPay()):
            self.wallet_money -= self.amountToPay()
            self.next_payment_premium = self.next_payment_premium + \
                timedelta(days=30)
            self.save()
            return True
        else:
            return False


class CommercialUser(PremiumUser):
    max_transactions = inf
    next_payment = models.DateField(auto_now_add=True)
    amount_to_pay = 5000

    @classmethod
    def create(cls, username, dob, email_id):
        # logger.info("user " + username + " created")
        user = cls(username=username, date_of_birth=dob,
                   email_id=email_id, plan='platinum', next_payment_premium=datetime.max)
        user.category = "commercial"
        user.save()
        timeline = Timeline(timeline_of=user)
        timeline.save()
        return user

    def check_pay(self):
        return(datetime.date(datetime.now()) < self.next_payment)

    def amountToPay(self):
        return amountToPay

    def paymentCycleInMonths(self):
        return 12

    def maxTransactions(self):
        return max_transactions

    def create_page(self, content):
        if(self.check_pay()):
            page = Page(admin=self, Content=content)
            page.save()
            return 'Page created'
        else:
            if(self.pay()):
                x = self.create_page(content)
                return 'The Amount due for continued service deducted from your wallet\n'+x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use commercial facilities without it'

    def send_message(self, UserId, content):
        if(self.check_pay()):
            to_user = CasualUser.objects.filter(pk=UserId)
            if not to_user.exists():
                return 'User does not exist'
            to_user = to_user[0]
            from_user = self
            msg = Private_Message(from_user=from_user,
                                  to_user=to_user, content=content)
            msg.save()
            return msg
            return 'Message sent'
        else:
            if(self.pay()):
                x = self.send_message(UserId, content)
                return 'The Amount due for continued service deducted from your wallet\n' + x
            else:
                return 'Please add money to your wallet as your payment is due.\nYou will not be able to use premium facilities without it'

    def pay(self):
        if(self.wallet_money > self.amount_to_pay):
            self.wallet_money -= self.amount_to_pay
            self.next_payment = self.next_payment + \
                timedelta(days=365)
            self.save()
            return True
        else:
            # print('add money to wallet comm')
            return False


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
    admin = models.OneToOneField(
        CommercialUser, on_delete=models.CASCADE, related_name='page')
    Content = models.CharField(max_length=500)

    def __str__(self):
        return "Page by "+str(self.admin)


class GroupMessage(models.Model):
    from_user = models.ForeignKey(
        CasualUser, related_name="from_message", on_delete=models.CASCADE
    )
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    admin = models.ForeignKey(PremiumUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CasualUser, related_name='member_of')
    name = models.CharField(max_length=20, default='New Group')
    join_requests = models.ManyToManyField(
        CasualUser, related_name='sent_join_request_to')
    can_send_join_requests = models.BooleanField(default=False)
    messages = models.ManyToManyField(
        GroupMessage, related_name='message_on')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name
