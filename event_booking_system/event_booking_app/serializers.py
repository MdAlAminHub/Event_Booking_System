from rest_framework import serializers
from .models import Event, Booking

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['event', 'ticket_type', 'quantity']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user  # Assign the user to the validated data
        return super().create(validated_data)