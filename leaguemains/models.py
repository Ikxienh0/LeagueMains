from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from riotapi_static.models import Champion


class LeagueMainsUserManager(BaseUserManager):

    def create_user(self, email, language='en_GB', password=None, nickname=None, region=None, summoner=None):
        if not email:
            raise ValueError('Users are required to have an email address')
        if not password:
            raise ValueError('Users are required to have a password')

        user = self.model(email=self.normalize_email(email), language=language, nickname=nickname, region=region, summoner=summoner)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, language='en_GB', password=None, nickname=None, region=None, summoner=None):
        if not email:
            raise ValueError('Superusers are required to have an email address')
        if not password:
            raise ValueError('Superusers are required to have a password')

        user = self.create_user(email, language=language, password=password, nickname=None, region=None, summoner=None)
        user.is_admin = True
        user.save(using=self._db)
        return user


class LeagueMainsUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=255, null=True)
    summoner = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)
    language = models.CharField(max_length=255, null=True)

    objects = LeagueMainsUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['language']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserChampionList(models.Model):
    pk_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField(default=False)
    fk_leaguemainsuser = models.ForeignKey(LeagueMainsUser)


class ChampionsInChampionList(models.Model):
    pk_id = models.AutoField(primary_key=True)
    fk_userchampionlist = models.ForeignKey(UserChampionList, related_name='champions', on_delete=models.CASCADE)
    fk_champion = models.ForeignKey(Champion)