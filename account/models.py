from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """注册用新的model，通过user字段对User表一一对应"""
    user = models.OneToOneField(User, unique=True, related_name="userprofile", on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(blank=True, max_length=20, null=True)
    
    def __str__(self):
        return 'User {}'.format(self.user.username)

class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, related_name="userinfo", on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return 'User {}'.format(self.user.username)

class Friendship(models.Model):
    followed = models.ForeignKey(User, related_name = 'followed', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)

    @classmethod
    def is_following(cls, u1, u2):
        if not u1.is_anonymous:
            return u1.followed.filter(follower__id=u2.id).count() > 0
        else:
            return False

    @classmethod
    def follow(cls, u1, u2):
        if (not cls.is_following(u1, u2)) and (u1 != u2):
            f = Friendship()
            f.followed = u1
            f.follower = u2
            f.save()
            


    @classmethod
    def unfollow(cls, u1, u2):
        if  cls.is_following(u1, u2):
            f = Friendship.objects.filter(followed=u1, follower=u2)
            f.delete()

