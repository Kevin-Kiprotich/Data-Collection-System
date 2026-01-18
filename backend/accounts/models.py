import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

# Create your models here.
class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=False)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES =[('OWNER', 'Owner'),('MANAGER','Manager')]
    username=None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, related_name='users', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True)
    phone_number= models.CharField(max_length=20, null=False)
    is_verified = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects = CustomUserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name_plural="Users"

class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, unique=True)
    code = models.CharField(max_length=6, null=False)
    trials = models.IntegerField(default=0, null=False)
    is_expired = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def has_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name_plural="OTP"
