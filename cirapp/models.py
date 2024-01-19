from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    registration_no = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    pimage = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self) -> str:
        return self.first_name


