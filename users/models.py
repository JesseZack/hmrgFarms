from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    GENDER = [("M", "Male"), ("F", "Female")]
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name

    class Meta:
        verbose_name = 'HMRG-Farms User'


# Create your models here.
class FarmSponsor(models.Model):
    user_acc = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=14)
    acc_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user_acc.first_name}  {self.user_acc.last_name}'


class Farmer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    primary_contact = models.CharField(max_length=14, unique=True)
    email_address = models.EmailField()
    date_of_birth = models.DateField()
    been_farmer_since = models.DateField()
    date_of_employment = models.DateField()

    def __str__(self):
        return f'{self.last_name}  {self.first_name}'


class FarmerHealthCondition(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50)
    description = models.TextField()


class OnSiteIncident(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    date_occurred = models.DateField()

    def __str__(self):
        return f'{self.title} {self.date_occurred}'

    class Meta:
        verbose_name = 'On-Site Incident'
        verbose_name_plural = 'On-Site Incidents'


class HMRGStaff(models.Model):
    user_acc = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=14)
    residential_address = models.CharField(max_length=150)
    digital_address = models.CharField(max_length=11)
    job_title = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField()

    def __str__(self):
        return f'{self.user_acc.first_name} {self.user_acc.last_name}'

    class Meta:
        verbose_name = 'HMRG Staff'
        verbose_name_plural = 'HMRG Staff'
