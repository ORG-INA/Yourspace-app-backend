from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin
)

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **kgwars):
        if not email:
            raise ValueError('El email debe ser obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **kgwars)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email, password=None, **kgwars):
        kgwars.setdefault('is_staff', False)
        kgwars.setdefault('is_superuser', False)
        return self._create_user(email, password, **kgwars)
    
    def create_superuser(self, email=None, password=None, **kgwars):
        kgwars.setdefault('is_staff', True)
        kgwars.setdefault('is_superuser', True)
        
        if kgwars.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if kgwars.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(email, password, **kgwars)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ["-date_joined"]
    