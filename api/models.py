import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from enum import Enum

from django.conf import settings

def choices(em):
    return [(e.value, e.name.replace("_"," ")) for e in em]

class Gender(Enum):
    Male = 1
    Female = 2
    Neutral = 3

class Region(Enum):
    Ashanti = 1
    Brong_Ahafo = 2
    Central = 3
    Eastern = 4
    Greater_Accra = 5
    Nothern = 6
    Upper_East = 7
    Upper_West = 8
    Volta = 9
    Western = 10

class PatientType(Enum):
    IN = 1
    OUT = 2

class Level(Enum):
    Primary = 1
    Secondary = 2
    Tertiary = 3

class ActiveQuerySet(models.QuerySet):
    def delete(self):
        self.update(update_fields=('is_active',))

class MUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_patient(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_patient', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_patient') is not True:
            raise ValueError('Superuser must have is_patient=True.')

        user = self._create_user(email, password, **extra_fields)

        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(email, password, **extra_fields)

        return user

    def active(self):
        return self.model.objects.filter(is_active=True)

    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)

class ActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(is_active=True)

    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)

class ActiveModel(models.Model):
    is_active = models.BooleanField(default=True, editable=False)

    class Meta:
        abstract = True

    def delete(self):
        self.is_active = False
        self.save()

    objects = ActiveManager()

class MUser(AbstractBaseUser):

    email = models.EmailField(verbose_name='email address', max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.PositiveIntegerField(choices=choices(Gender), default=1)
    date_of_birth = models.DateField(default=datetime.date.today)
    address = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=12, db_index=True)
    is_active = models.BooleanField(default=True, help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)

    objects = MUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'user'
        verbose_name = 'users'

    def has_perm(self, perm, obj=None):
       return self.is_superuser

    def has_module_perms(self, app_label):
       return self.is_superuser

    def __str__(self):
        self.email

    



        

class Patient(ActiveModel):
    patient_no = models.CharField(max_length=10, db_index=True, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(db_index=True, unique=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.IntegerField(choices=choices(Region))
    patient_type = models.IntegerField(choices=choices(PatientType), default=2)
    
    class Meta:
        db_table = 'patient'
        verbose_name = 'patients'
        unique_together = ('patient_no', 'slug')

    def __str__(self):
        return self.patient_no
