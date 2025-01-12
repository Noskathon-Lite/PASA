from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=45)
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('prof', 'Prof'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')


class User(CustomUser):
    best_fit_profs = models.ManyToManyField(
        'Prof',
        related_name= 'matched_by_user',
        blank=True
    )

    def __str__(self):
        return self.username



class Prof(CustomUser):
    verified = models.BooleanField(default=False)
    best_fit_users = models.ManyToManyField(
        'User',
        related_name='matched_by_profs',
        blank=True
    )

    def __str__(self):
        return self.username



class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userdata')
    questionNo = models.IntegerField()
    questionText = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"Userdata of {self.user.username}"
    


class ProfData(models.Model):
    prof = models.ForeignKey(Prof, on_delete=models.CASCADE, related_name='profdata')
    questionNo = models.IntegerField()
    questionText = models.TextField()
    answer = models.TextField()

#    class Meta:
#        ordering = ['questionNo']

    def __str__(self):
        return f"Profdata of {self.prof.username}"