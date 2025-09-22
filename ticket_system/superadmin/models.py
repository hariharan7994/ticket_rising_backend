from django.db import models
from django.contrib.auth.models import AbstractUser

# ---------------USER MODEL---------------
class User(AbstractUser):
    is_superadmin = models.BooleanField(default=False)
    is_supporter = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    def _str_(self):
        return self.username
    
class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Supporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.user.username
    

class Customuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def _str_(self):
        return self.user.username    
    
