from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models
from django.utils import timezone

from django.db.models import F
from django.db import transaction

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_vip = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set', 
        blank=True,
    )

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    regular_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    vip_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    early_bird_discount = models.DecimalField(max_digits=5, decimal_places=2)
    early_bird_deadline = models.DateTimeField()
    regular_ticket_count = models.PositiveIntegerField(default=0, db_index=True)  # Indexed for performance
    vip_ticket_count = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    ticket_type = models.CharField(max_length=10, choices=[('regular', 'Regular'), ('vip', 'VIP')], db_index=True)
    quantity = models.PositiveIntegerField()
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            current_time = timezone.now()  # Get the current time for comparison
            if self.ticket_type == 'regular':
                if current_time <= self.event.early_bird_deadline:
                    self.price_paid = self.event.regular_ticket_price * (1 - self.event.early_bird_discount / 100)
                else:
                    self.price_paid = self.event.regular_ticket_price
                if self.event.regular_ticket_count < self.quantity:
                    raise ValueError('Not enough regular tickets available')
                Event.objects.filter(id=self.event.id).update(regular_ticket_count=F('regular_ticket_count') - self.quantity)
            elif self.ticket_type == 'vip':
                if current_time <= self.event.early_bird_deadline:
                    self.price_paid = self.event.vip_ticket_price * (1 - self.event.early_bird_discount / 100)
                else:
                    self.price_paid = self.event.vip_ticket_price
                if self.event.vip_ticket_count < self.quantity:
                    raise ValueError('Not enough VIP tickets available')
                Event.objects.filter(id=self.event.id).update(vip_ticket_count=F('vip_ticket_count') - self.quantity)
            super().save(*args, **kwargs)

  
