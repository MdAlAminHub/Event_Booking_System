from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, Booking


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_vip', 'is_staff', 'is_active')
    list_filter = ('is_vip', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('VIP Info', {'fields': ('is_vip',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_vip', 'is_active', 'is_staff')}
        ),
    )
# Admin for Event model
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'regular_ticket_count', 'vip_ticket_count', 'early_bird_deadline')
    list_filter = ('date',)
    search_fields = ('name',)

# Admin for Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket_type', 'quantity', 'price_paid', 'booking_date')
    list_filter = ('ticket_type', 'event', 'booking_date')
    search_fields = ('user__username', 'event__name')

