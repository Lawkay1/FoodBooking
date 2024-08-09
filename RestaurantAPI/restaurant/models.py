from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('chef', 'Chef'),
        ('user', 'User'),
    ]

    COUNTRY_CHOICES = [
        ('NG', 'Nigeria'),
        ('GH', 'Ghana'),
        ('SA', 'South Africa'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField()
    venue = models.CharField(max_length=255)
    guests = models.IntegerField()

    def __str__(self):
        return f'Booking by {self.user.username} for {self.menu.name}'
